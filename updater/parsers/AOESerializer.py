import re
import os
import pandas as pd
import numpy as np
import pickle

class AOESerializer:

	"""
	Takes user logs logged by vrelay. Transforms them into a dictionary of AOEs.
	"""

	def parseLogs(self) -> (pd.DataFrame, pd.DataFrame):

		"""
		Find all the user logs, extract showEffect and AOE.
		Remove showEffect logs that do not correspond with an actual AOE.
		"""

		logPath = '../userLogs/'
		showEffectRegex = re.compile('enemy\s([0-9]+).+\nShowEffect\s([0-9]+.[0-9]+).+color\s(-?[0-9]+).+\nx:\s([0-9]+.[0-9]+)\sy:\s([0-9]+.[0-9]+).+\n')
		aoeRegex = re.compile('Aoe\s([0-9]+.[0-9]+)\sradius\s([0-9]+\.[0-9])\sdamage\s([0-9]+)\s.+origType\s([0-9]+)\nx:\s([0-9]+.[0-9]+)\sy:\s([0-9]+.[0-9]+)')
		showEffectDict = {
			'id' : [], 'file': [], 'time': [], 'objectType': [], 'color': [], 'x': [], 'y': []
		}
		aoeDict = {
			'id' : [], 'file': [], 'time': [], 'radius': [], 'damage': [], 'objectType': [], 'x': [], 'y': []
		}

		for root, dirs, files in os.walk(logPath):
			for file in files:
				identifier = re.sub(logPath, "", root)
				fhandle = open(root + '/' + file, "r").read()
				for e in showEffectRegex.finditer(fhandle):
					showEffectDict['id'].append(identifier)
					showEffectDict['file'].append(file)
					showEffectDict['time'].append(e.group(2))
					showEffectDict['objectType'].append(e.group(1))
					showEffectDict['color'].append(e.group(3))
					showEffectDict['x'].append(round(float(e.group(4)), 6))
					showEffectDict['y'].append(round(float(e.group(5)), 6))
					
				for e in aoeRegex.finditer(fhandle):
					aoeDict['id'].append(identifier)
					aoeDict['file'].append(file)
					aoeDict['time'].append(e.group(1))
					aoeDict['radius'].append(e.group(2))
					aoeDict['damage'].append(e.group(3))
					aoeDict['objectType'].append(e.group(4))
					aoeDict['x'].append(round(float(e.group(5)), 6))
					aoeDict['y'].append(round(float(e.group(6)), 6))

		# drop non AOE showEffects
		nonAoeEffects = [
			('28704', '-16640'), # dr terrible, greenpotion
			('28705', '-16640'), # dr terrible clone 1, greenpotion
			('28706', '-16640'), # dr terrible clone 2, greenpotion
		]

		effectDF = pd.DataFrame(showEffectDict)
		# remove huntress and assassin
		effectDF = effectDF[(effectDF.objectType != '802') & (effectDF.objectType != '800')].reset_index(drop = True)
		for remove in nonAoeEffects:
			effectDF = effectDF.drop(index = effectDF[(effectDF.objectType == remove[0]) & (effectDF.color == remove[1])].index).reset_index(drop = True)
		aoeDF = pd.DataFrame(aoeDict)

		return effectDF, aoeDF

	"""
	Given a showEffect df and AOE df, use a greedy algorithm to match corresponding showEffects with the proper AOE.
	Returns the merged dataframe.

	CAVEATS
	this greedy algorithm doesn't work if there is showEffect but the next AOE was not seen. 
	This is because suppose there are two show effects, same location but only one AOE. if both are before that AOE, then the first show effect will be matched. 
	But what if it is the second showEffect, not the first one?
	- mitigation: use median, round nearest tick

	this will also fail in circumstances where data isn't actually missing, but the first showEffect is not tied with an AoE (like dr terrible greenpotion)
	- mitigation: clean up showEffect beforehand.

	btw, we're not using join because if there's 3 show effects at the same time/location, we're going to get 9 data points. A good example here is Zol Lieutenant L/R.
	However, we have overly matched the showEffects to multiple AOE's, which is incorrect.
	We cannot tell apriori which showEffect should be matched with the AOE. Thus, we will use this greedy algorithm (it's close to a more selective left join) as a solution (with median / data cleaning)
	"""
	def mergeEffectAndAoe(self, effectDF, aoeDF) -> pd.DataFrame:

		mergedDict = {
			'id': [], 'file': [], 'effectTime': [], 'aoeTime': [], 'objectType': [], 
			'color': [], 'x': [], 'y': [], 'radius': [], 'damage':[], 'hangTime': [],
			'effectIndex': [], 'aoeIndex': []
		}
		noAOEIndex = []
		aoeBeforeEffect = []

		for row in effectDF.itertuples():

			# match current AOE with a showEffect
			sliced = aoeDF[(aoeDF.objectType == row.objectType) & (aoeDF.x == row.x) & (aoeDF.y == row.y)]
			# if this is an showEffect with no AOE logged (you walked into viewing range of AOE but didn't see the throw)
			if sliced.shape[0] == 0:
				noAOEIndex.append(row.Index)
				continue
			# get time diffs
			searchThis = sliced.time.astype(float) - float(row.time)
			# find the soonest AOE after showEffect
			# if there are no matches (these cases are when the AoE is logged before showEffect, which we will not trust)
			idx = searchThis[searchThis > 0]
			if idx.shape[0] == 0:
				aoeBeforeEffect.append(row.Index)
				continue
			idx = idx.idxmin()
			# this greedy algorithm matches the most recent AOE's correctly, assuming that we get the show effect packets in the correct order.
			# since this a tcp protocol, we can assume this to be true if the server logic is consistent.
			# after matching, we must remove as we have already matched this AoE
			aoeDF = aoeDF.drop(aoeDF.index[idx]).reset_index(drop = True)
			mergedDict['id'].append(row.id)
			mergedDict['file'].append(row.file)
			mergedDict['effectTime'].append(row.time)
			mergedDict['aoeTime'].append(sliced.loc[idx, 'time'])
			mergedDict['objectType'].append(int(row.objectType))
			mergedDict['color'].append(int(row.color))
			mergedDict['x'].append(row.x)
			mergedDict['y'].append(row.y)
			mergedDict['radius'].append(float(sliced.loc[idx, 'radius']))
			mergedDict['damage'].append(int(sliced.loc[idx, 'damage']))
			mergedDict['hangTime'].append(float(searchThis.loc[idx]))
			
			# which indices were joined together? for debugging
			mergedDict['effectIndex'].append(row.Index)
			mergedDict['aoeIndex'].append(idx)

		merged = pd.DataFrame(mergedDict)
		merged.to_csv("joinedData.csv", index = False)
		return merged

	# round floats to the nearest tick (two-tenths of a second)
	def roundNearestTick(self, i: float) -> float:
		if i < 0.1:
			return 0.2
		r = np.arange(0.1, 2.1, 0.2)
		for j in range(len(r) - 1):
			if r[j] < i and i < r[j+1]:
				return round((r[j] + r[j+1]) / 2, 2)

	# this is where we will choose highest damaging AoE. It's not the best, but it's safe.
	# need to research how to predict smaller ones
	def serializeAOE(self, g: pd.DataFrame):
		
		# for debugging, don't actually use this
		d = pd.DataFrame(columns = g.columns)
		"""
		{
		objectType : {
			effectColor: {
				damage,
				radius,
				hangTime
				}
			}
		}
		"""
		aoeDict = {}
		# for each enemy
		for obj in g.objectType.unique():
			sliced = g[g.objectType == obj]
			# first time seeing this enemy
			aoeDict.update({int(obj) : {}})
			# for each unique color (all we can get from showEffect)
			for color in sliced.color.unique():
				maxidx = sliced[sliced.color == color].damage.idxmax()
				aoeDict[obj].update(
					{int(color) : {
						'damage': int(sliced.loc[maxidx, 'damage']),
						'radius': float(sliced.loc[maxidx, 'radius']),
						'hangTime': float(sliced.loc[maxidx, 'hangTime'])
					}
					}
				)
				d = d.append(sliced.loc[sliced[sliced.color == color].damage.idxmax()], ignore_index = True)
				
		d['objectType'] = d['objectType'].astype(int)
		d['color'] = d['color'].astype(int)
		d['damage'] = d['damage'].astype(int)
		
		return d, aoeDict

	def main(self):

		# clean up logs; get showEffect and AOE dataframes
		print("Parsing log files...")
		effectDF, aoeDF = self.parseLogs()
		print("Finished parsing. Merging dataframes...")
		# merge the two dataframes. save a copy tho
		merged = self.mergeEffectAndAoe(effectDF, aoeDF)
		# collapse down data to unique AOE's
		print("Finished merging. Selecting highest damaging AOE's (up to apriori knowledge before AOE land)")
		g = merged.groupby(['objectType', 'color', 'damage', 'radius'])['hangTime'].agg(['median', 'count']).reset_index()
		g = g.rename(columns = {'median': 'hangTime', 'count': 'numSamples'})
		# round ticks to nearest tick
		g['hangTime'] = g['hangTime'].apply(self.roundNearestTick)
		maxDamageAOE, aoeDict = self.serializeAOE(g)
		maxDamageAOE['objectType'] = maxDamageAOE['objectType'].astype(int)
		maxDamageAOE['color'] = maxDamageAOE['color'].astype(int)
		maxDamageAOE['damage'] = maxDamageAOE['damage'].astype(int)
		with open("../../bin/AoeDictionary.pkl", "wb") as f:
			pickle.dump(aoeDict, f)
		print("Saved AOE dictionary.")


def main():
	c = AOESerializer()
	c.main()

if __name__ == '__main__':
	main()

