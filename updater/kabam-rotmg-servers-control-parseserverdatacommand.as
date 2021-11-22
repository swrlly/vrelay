 
package kabam.rotmg.servers.control
{
   import kabam.rotmg.servers.api.Server;
   import kabam.rotmg.servers.api.ServerModel;
   
   public class ParseServerDataCommand
   {
       
      
      [Inject]
      public var servers:ServerModel;
      
      [Inject]
      public var data:XML;
      
      public function ParseServerDataCommand()
      {
         super();
      }
      
      public static function makeLocalhostServer() : Server
      {  
         return new Server().setName("Proxy").setAddress("127.0.0.1").setPort(2050).setLatLong(Infinity,Infinity).setUsage(0).setIsAdminOnly(false);
      }
      
      public function execute() : void
      {
         this.servers.setServers(this.makeListOfServers());
      }
      
      private function makeListOfServers() : Vector.<Server>
      {
         var _loc2_:* = null;
         var _loc3_:XMLList = this.data.child("Servers").child("Server");
         var _loc1_:Vector.<Server> = new Vector.<Server>(0);
         var _loc5_:int = 0;
         var _loc4_:* = _loc3_;
         _loc1_.push(makeLocalhostServer());
         for each(_loc2_ in _loc3_)
         {
            _loc1_.push(this.makeServer(_loc2_));
         }
         return _loc1_;
      }
      
      private function makeServer(param1:XML) : Server
      {
         return new Server().setName(param1.Name).setAddress(param1.DNS).setPort(2050).setLatLong(Number(param1.Lat),Number(param1.Long)).setUsage(param1.Usage).setIsAdminOnly(param1.hasOwnProperty("AdminOnly"));
      }
   }
}
