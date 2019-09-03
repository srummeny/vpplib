"""
Info
----
This file contains the basic functionalities of the VPPComponent class.
This is the mother class of all VPPx classes

"""

class VPPThermalEnergyStorage(object):
    
    # 
    def __init__(self, timebase, environment = None, userProfile = None, 
                 target_temperature = 60, hysteresis = 3, mass = 300, cp = 4.2, 
                 heatloss_per_day = 0.13 ):
        
        """
        Info
        ----
        ...
        
        Parameters
        ----------
        
        The parameter timebase determines the resolution of the given data. 
        Furthermore the parameter environment (VPPEnvironment) is given to provide weather data and further external influences. 
        To account for different people using a component, a use case (VPPUseCase) can be passed in to improve the simulation.
        	
        Attributes
        ----------
        
        ...
        
        Notes
        -----
        
        ...
        
        References
        ----------
        
        ...
        
        Returns
        -------
        
        ...
        
        """
    
        # Configure attributes
        self.unit = "kW"
        self.dataResolution = timebase
        self.environment = environment
        self.userProfile = userProfile
        self.target_temperature = target_temperature
        self.current_temperature = target_temperature - hysteresis
        self.hysteresis = hysteresis
        self.mass = mass
        self.cp = cp
        self.state_of_charge = mass * cp * (self.current_temperature + 273.15)
        #Aus Datenblättern ergibt sich, dass ein Wärmespeicher je Tag rund 10% Bereitschaftsverluste hat (ohne Rohrleitungen!!)
        self.heatloss_per_timestep = 1 - (heatloss_per_day / (24 * (60 / timebase)))
        self.needs_loading = False
    
    def charge(self, size_of_charge):
        #Formula: E = m * cp * T
        #     <=> T = E / (m * cp)
        self.state_of_charge -= size_of_charge * 1000 * self.heatloss_per_timestep
        self.current_temperature = (self.state_of_charge / (self.mass * self.cp)) - 273.15
        
        if self.current_temperature <= (self.target_temperature - self.hysteresis): 
            self.needs_loading = True
            
        if self.current_temperature >= (self.target_temperature + self.hysteresis): 
            self.needs_loading = False
            
        return self.current_temperature, self.needs_loading       
        
    def valueForTimestamp(self, timestamp):
        
        """
        Info
        ----
        This function takes a timestamp as the parameter and returns the 
        corresponding value for that timestamp. 
        A positiv result represents a load. 
        A negative result represents a generation. 
        
        This abstract function needs to be implemented by child classes.
        Raises an error since this function needs to be implemented by child classes.
        
        Parameters
        ----------
        
        ...
        	
        Attributes
        ----------
        
        ...
        
        Notes
        -----
        
        ...
        
        References
        ----------
        
        ...
        
        Returns
        -------
        
        ...
        
        """
    
        raise NotImplementedError("valueForTimestamp needs to be implemented by child classes!")
    

    def observationsForTimestamp(self, timestamp):
        
        """
        Info
        ----
        This function takes a timestamp as the parameter and returns a 
        dictionary with key (String) value (Any) pairs. 
        Depending on the type of component, different status parameters of the 
        respective component can be queried. 
        
        For example, a power store can report its "State of Charge".
        Returns an empty dictionary since this function needs to be 
        implemented by child classes.
        
        Parameters
        ----------
        
        ...
        	
        Attributes
        ----------
        
        ...
        
        Notes
        -----
        
        ...
        
        References
        ----------
        
        ...
        
        Returns
        -------
        
        ...
        
        """
    
        return {}


    def prepareTimeSeries(self):
        
        """
        Info
        ----
        This function is called to prepare the time series for generations and 
        consumptions that are based on a non controllable data series. 
        An empty array is stored for generation units that are independent of 
        external influences.
        
        Setting an empty array. 
        Override this function if generation or consumption is based on data series.
        
        Parameters
        ----------
        
        ...
        	
        Attributes
        ----------
        
        ...
        
        Notes
        -----
        
        ...
        
        References
        ----------
        
        ...
        
        Returns
        -------
        
        ...
        
        """

        self.timeseries = []
        