#!/usr/bin/env python

#######################################################
# ships.py - Classes for all in game ships.
# Authors : Justin Sweitzer, Ben Sweitzer
# Started development 04/04/2013
# Version 0.1
#
#######################################################


import components, time, os

class Fighter():
    pass

class CapitalShip():
    def __init__(self, VesselClass, root):
        if VesselClass == 'Explorer':  
            torpedos = 10
            rev = 'Mk1'
            forTubes = 2
            aftTubes = 1
            fighters = 5
            turrets = 2
            MaxCores = 2
            PowerPlants = 1
            MaxEngines = 2
            WarpEngines = 1
            enginetype = 'EM'
            coretype = 'Nuclear'
        self.Model = os.path.join(root,'ships/models/ships/fighter.egg')    
        self.Class = VesselClass
        self.MaxFighters = fighters
        self.Fighters = [ Fighter() for i in range(0,self.MaxFighters) ]
        
        self.NumForwardTubes = forTubes
        self.NumAftTubes = aftTubes     
        self.MaxTorpedos = torpedos
        #self.Torpedos = [ components.Torpedo(rev) for i in range(0,self.MaxTorpedos) ]
         
        self.MaxPowerPlants = MaxCores
        self.NumPowerPlants = PowerPlants
        self.PowerPlants = [ components.PowerPlant(coretype) for i in range(0,PowerPlants) ]
        self.MaxOutput = sum((self.PowerPlants[i].Output for i in range(0,PowerPlants)))
        self.FuelCapacity = sum((self.PowerPlants[i].Capacity for i in range(0,PowerPlants)))
        self.Fuel = self.FuelCapacity
        
        self.MaxWarpEngines = MaxEngines
        self.NumWarpEngines = WarpEngines
        self.WarpEngines = [ components.WarpEngine(enginetype) for i in range(0,WarpEngines) ]
        self.WarpPowerConsumption = sum(((self.WarpEngines[i].PowerConsumption) for i in range(0,WarpEngines)))
        self.MaxWarp = (0.5*(sum(self.PowerPlants[i].Output for i in range(0,self.NumPowerPlants)))**0.25 + self.NumWarpEngines)*(self.WarpEngines[0].Efficiency+self.NumWarpEngines/20.) 
         
        self.CurrentWarpFactor = 0
        self.Coordinates = (0.0,0.0,0.0)
        
    def WarpToSystem(self,System,WarpFactor):
        if WarpFactor > self.MaxWarp:
            print "Warp factor out of range of current capabilities"
        else:
            while self.Fuel > 0 and self.Coordinates != System.Coordinates:
                distance = (sum((self.Coordinates[i] - System.Coordinates[i])**2 for i in range(0,3)))**0.5
                if self.Fuel - distance*self.WarpPowerConsumption < 0:
                    print 'Not enough fuel for this trip'
                    
                gametimetaken = int((distance/WarpFactor**6.75)*12) # Time taken for trip in months
                timetaken = int((distance/(WarpFactor**6.75)*5.76)) # Gives 30 s for crossing quadrant at w 3 
                print 'Initializing warp engines'
                self.CurrentWarpFactor = WarpFactor
                time.sleep(1)
                print 'Current velocity is warp %f' % (self.CurrentWarpFactor)
                print 'Warping'
                for i in range(0,timetaken):
                    print '.'
                    time.sleep(1)
                print 'Arriving at coordinates %s, %s' % (System.Coordinates, System.Name)
                self.System = System
                self.Fuel -= distance * self.WarpPowerConsumption
                self.Coordinates = self.System.Coordinates
            return(gametimetaken)   #Calling this function will advance the gametime by gametimetaken
            
    def AddEngine(self,Type):
        success = 0
        while success == 0:
            if Type != self.WarpEngines[0].Type:
                print 'All engines must be of the same type.'
                print 'Installing %s type engine instead' % (self.WarpEngines[0].Type)
                Type = self.WarpEngines[0].Type
                success = 0
                pass
            else:
                self.WarpEngines.append(components.WarpEngine(Type))
                self.NumWarpEngines = len(self.WarpEngines)
                success = 1
                
        self.MaxWarp = (0.5*(sum(self.PowerPlants[i].Output for i in range(0,self.NumPowerPlants)))**0.25 + self.NumWarpEngines)*(self.WarpEngines[0].Efficiency+self.NumWarpEngines/20.) 

                   
            




class Frigate():
    pass

class Cruiser():
    pass

class Destroyer():
    pass

# The player will only have a capital ship that can be upgraded/upsized to various 'classes'
# Classes should be named something cool like 'Ticonderoga', etc.
# Fighter chassis launchable via capital ship, replace kamikaze/guided drone concept from Lightspeed with Torpedos.
# Should torpedos use a chassis?
# Individual components will be upgradable within the same 'class' of vessel

# The other types of vessels should be reserved for aliens.
 