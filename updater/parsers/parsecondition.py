import re

s = """      public function isQuiet() : Boolean
      {
         return (this.condition_[0] & 2) != 0;
      }
      
      public function isWeak() : Boolean
      {
         return (this.condition_[0] & 4) != 0;
      }
      
      public function isSlowed() : Boolean
      {
         return (this.condition_[0] & 8) != 0;
      }
      
      public function isSick() : Boolean
      {
         return (this.condition_[0] & 16) != 0;
      }
      
      public function isDazed() : Boolean
      {
         return (this.condition_[0] & 32) != 0;
      }
      
      public function isStunned() : Boolean
      {
         return (this.condition_[0] & 64) != 0;
      }
      
      public function isBlind() : Boolean
      {
         return (this.condition_[0] & 128) != 0;
      }
      
      public function isDrunk() : Boolean
      {
         return (this.condition_[0] & 512) != 0;
      }
      
      public function isConfused() : Boolean
      {
         return (this.condition_[0] & 1024) != 0;
      }
      
      public function isStunImmune() : Boolean
      {
         return (this.condition_[0] & 2048) != 0
      }
      
      public function isInvisible() : Boolean
      {
         return (this.condition_[0] & 4096) != 0;
      }
      
      public function isParalyzed() : Boolean
      {
         return (this.condition_[0] & 8192) != 0;
      }
      
      public function isSpeedy() : Boolean
      {
         return (this.condition_[0] & 16384) != 0;
      }
      
      public function isNinjaSpeedy() : Boolean
      {
         return (this.condition_[0] & 268435456) != 0;
      }
      
      public function isHallucinating() : Boolean
      {
         return (this.condition_[0] & 256) != 0;
      }
      
      public function isHealing() : Boolean
      {
         return (this.condition_[0] & 131072) != 0;
      }
      
      public function isDamaging() : Boolean
      {
         return (this.condition_[0] & 262144) != 0;
      }
      
      public function isBerserk() : Boolean
      {
         return (this.condition_[0] & 524288) != 0;
      }
      
      public function isPaused() : Boolean
      {
         return (this.condition_[0] & 1048576) != 0;
      }
      
      public function isStasis() : Boolean
      {
         return (this.condition_[0] & 2097152) != 0;
      }
      
      public function isInvincible() : Boolean
      {
         return (this.condition_[0] & 8388608) != 0;
      }
      
      public function isInvulnerable() : Boolean
      {
         return (this.condition_[0] & 16777216) != 0;
      }
      
      public function isArmored() : Boolean
      {
         return (this.condition_[0] & 33554432) != 0;
      }
      
      public function isArmorBroken() : Boolean
      {
         return (this.condition_[0] & 67108864) != 0;
      }
      
      public function isArmorBrokenImmune() : Boolean
      {
         return (this.condition_[0] & 65536) != 0;
      }
      
      public function isSlowedImmune() : Boolean
      {
         return (this.condition_[0] & 2147483648) != 0;
      }
      
      public function isUnstable() : Boolean
      {
         return (this.condition_[0] & 536870912) != 0;
      }
      
      public function isSwiftness() : Boolean
      {
         return (this.condition_[1] & 16) != 0;
      }
      
      public function isDarkness() : Boolean
      {
         return (this.condition_[0] & 1073741824) != 0;
      }
      
      public function isParalyzeImmune() : Boolean
      {
         return (this.condition_[1] & 2) != 0;
      }
      
      public function isDazedImmune() : Boolean
      {
         return (this.condition_[1] & 1) != 0;
      }
      
      public function isPetrified() : Boolean
      {
         return (this.condition_[1] & 4) != 0;
      }
      
      public function isPetrifiedImmune() : Boolean
      {
         return (this.condition_[1] & 8) != 0;
      }
      
      public function isCursed() : Boolean
      {
         return (this.condition_[1] & 32) != 0;
      }
      
      public function isCursedImmune() : Boolean
      {
         return (this.condition_[1] & 64) != 0;
      }
      
      public function isHidden() : Boolean
      {
         return (this.condition_[1] & 32768) != 0;
      }
      
      public function isSamuraiBerserk() : Boolean
      {
         return (this.condition_[1] & 8388608) != 0;
      }
      
      public function isRelentless() : Boolean
      {
         return (this.condition_[1] & 67108864) != 0;
      }
      
      public function isVengeance() : Boolean
      {
         return (this.condition_[1] & 134217728) != 0;
      }
      
      public function isAlliance() : Boolean
      {
         return (this.condition_[1] & 536870912) != 0;
      }
      
      public function isGrasp() : Boolean
      {
         return (this.condition_[1] & 4194304) != 0;
      }
      
      public function isBravery() : Boolean
      {
         return (this.condition_[1] & 262144) != 0;
      }
      
      public function isBleeding() : Boolean
      {
         return (this.condition_[0] & 32768) != 0;
      }
      
      public function isExhausted() : Boolean
      {
         return (this.condition_[1] & 524288) != 0;
      }
      
      public function isJacketOffense() : Boolean
      {
         return (this.condition_[1] & 2) != 0;
      }
      
      public function isJacketDefense() : Boolean
      {
         return (this.condition_[1] & 4) != 0;
      }
      
      public function isEmpoweredImmunity() : Boolean
      {
         return (this.condition_[2] & 8) != 0;
      }
      
      public function isConfusedImmunity() : Boolean
      {
         return (this.condition_[2] & 16) != 0;
      }
      
      public function isWeakImmunity() : Boolean
      {
         return (this.condition_[2] & 32) != 0;
      }
      
      public function isBlindImmunity() : Boolean
      {
         return (this.condition_[2] & 64) != 0;
      }
      
      public function isQuietImmunity() : Boolean
      {
         return (this.condition_[2] & 128) != 0;
      }
      
      public function isBleedingImmunity() : Boolean
      {
         return (this.condition_[2] & 256) != 0;
      }
      
      public function isSickImmunity() : Boolean
      {
         return (this.condition_[2] & 512) != 0;
      }
      
      public function isDrunkImmunity() : Boolean
      {
         return (this.condition_[2] & 1024) != 0;
      }
      
      public function isHallucinatingImmunity() : Boolean
      {
         return (this.condition_[2] & 2048) != 0;
      }
      
      public function isHexedImmunity() : Boolean
      {
         return (this.condition_[2] & 4096) != 0;
      }
      
      public function isUnstableImmunity() : Boolean
      {
         return (this.condition_[2] & 8192) != 0;
      }
      
      public function isDarknessImmunity() : Boolean
      {
         return (this.condition_[2] & 16384) != 0;
      }
      
      public function isExhaustedImmunity() : Boolean
      {
         return (this.condition_[2] & 32768) != 0;
      }
      
      public function isStasisImmune() : Boolean
      {
         return (this.condition_[2] & 4194304) != 0;
      }
      
      public function isCorruptedImmune() : Boolean
      {
         return (this.condition_[2] & 65536) != 0;
      }"""

def process(num):
   x = re.findall("is.+?\n.+?\n.+?this\.condition\_\[{}\].+?[0-9]+?\)".format(num), s)
   print("effect{}".format(num) +  " = {")
   for c in range(len(x)):
      name = re.search("[A-Za-z].+\(", x[c][2:]).group()[:-1]
      value = re.search("[0-9]+", x[c][len(x[c])-2::-1]).group()[::-1]
      if c != len(x) - 1:
         print("\t\"" + name + "\" : " + value + ",")
      else:
         print("\t\"" + name + "\" : " + value + ",")
   print("}")

def main():
   for i in range(0, 3):
      process(i)
      print()

if __name__ == "__main__":
   main()

