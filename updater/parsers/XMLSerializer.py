import os
import xml.etree.ElementTree as ET
import pickle

path = "../binaryData/"

class Serializer:

    def getValue(self, e : ET.Element):
        if e is not None:
            return e.text
        return e


class GroundTileSerializer(Serializer):

    def createTileDictionary(self):
        
        tileDict = {}

        for i in os.listdir(path):

            if "GroundCXML" in i:

                tree = ET.parse(path + i)

                # for each object
                for obj in tree.findall("Ground"):
                    
                    groundType = int(obj.get("type"), 16)
                    mindmg = int(self.getValue(obj.find("MinDamage"))) if obj.find("MinDamage") is not None else 0
                    maxdmg = int(self.getValue(obj.find("MaxDamage"))) if obj.find("MaxDamage") is not None else 0
                    tile = {"minDamage" : mindmg, "maxDamage" : maxdmg}
                    tileDict.update({groundType : tile})
                    
        print("Successfully serialized {} tiles.".format(len(tileDict)))
        
        with open("../../bin/TileDictionary.pkl", "wb") as f:
            pickle.dump(tileDict, f)
            
        return tileDict
        

class BulletSerializer(Serializer):
    
    # key - (objectType, projectileID)
    # value - damage, conditioneffect

    def createBulletDictionary(self):
        
        bulletDict = {}
        nameDict = {}

        for i in os.listdir(path):

            if "XML" in i:

                tree = ET.parse(path + i)

                # for each object
                for obj in tree.findall("Object"):

                    objectType = int(obj.get("type"), 16)
                    name = obj.get("id")
                    nameDict.update({objectType : name})

                    add = False

                    # if there is a projectile
                    for projectile in obj.findall("Projectile"):
                        projectileID = int(projectile.get("id")) if projectile.get("id") is not None else 0
                        damage = int(self.getValue(projectile.find("Damage"))) if projectile.find("Damage") is not None else 0
                        conditionEffect = self.getValue(projectile.find("ConditionEffect"))
                        armorPierce = True if projectile.find("ArmorPiercing") is not None else False
                        newBullet = {"damage" : damage, "conditionEffect" : conditionEffect, "armorPiercing" : armorPierce}
                        bulletDict.update({(objectType, projectileID) : newBullet})
                    else:
                        pass
                        

                    
        print("Successfully serialized {} enemies.".format(len(set([x[0] for x in bulletDict.keys()]))))            
        print("Successfully serialized {} bullets.".format(len(bulletDict)))
        
        with open("../../bin/BulletDictionary.pkl", "wb") as f:
            pickle.dump(bulletDict, f)

        with open("../../bin/NameDictionary.pkl", "wb") as f:
            pickle.dump(nameDict, f)
            
        return bulletDict, nameDict

def main():
    g = GroundTileSerializer()
    g.createTileDictionary()
    b = BulletSerializer()
    b.createBulletDictionary()

if __name__ == "__main__":
    main()