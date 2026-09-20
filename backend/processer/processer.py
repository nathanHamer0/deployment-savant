import pickle
import abc
PITCH_TYPES = [
"FF",
"SI",
"FC",
"CH",
"FS",
"FO",
"SC",
"CU",
"KC",
"CS",
"SL",
"ST",
"SV",
"KN",
"EP",
"FA",
"IN",
"PO",
"UN"
] 

class Pack(abc.ABC):
    """A repackaging of any specified-statistic (entry) of profiler.py's outputted profiles dictionary intended 
    for further data-processing.
    """
 
    def get_all_data(self):
        """Returns internal data of this pack.

        Returns:
            dict: parameter-keyed nD dictionary containing player-tupled frequencies.
        """
        return self.data
 
    def sort(self, stat_param_key01, stat_param_key02=""):
        """Sorts data for a specified-statistic.

        Args:
            stat_param_key01 (str): parameter for specified-statistic.
            stat_param_key02 (str, optional): parameter for specified-statistic.
        """
        self.get_data(stat_param_key01, stat_param_key02).sort(key=lambda x: x[1])
    
    def show(self):
        """Display pack to terminal.
        """
        print(self.data)
    
    # FIXME: the need to repackage begs the question: Should'nt the data be initially packaged in the optimal way at its first inflection in profiler.py...?
    def repackage(self, stat_profiles, stat_param_key01, stat_param_key02=""):
        """Rearranges player-keyed (parameter-keyed) dictionaries of specified-statistic into an equivalent parameter-keyed (player-tupled) dictionary.

        Args:
            stat_profiles (dict[dict]): profiles for specified-statistic.
            stat_param_key01 (str): parameter for specified-statistic.
            stat_param_key02 (str, optional): parameter for specified-statistic.
        """
        for player in stat_profiles:
            freq = 0.0
            
            # Extract frequency if player qualifies for paramaterized statistic
            player_stat_profile = stat_profiles[player]
            if stat_param_key01 in player_stat_profile and (stat_param_key02 in player_stat_profile or not stat_param_key02):
                freq = self.extract_data(stat_profiles, player, stat_param_key01, stat_param_key02)
                
            self.get_data(stat_param_key01, stat_param_key02).append((player, freq))

    def percentalize(self):
        """Percentalizes player-specific frequencies for a specified-statistic.
        
        WARNING: the mutations of this method are irreversible.
        """
        
        # Sort atps
        self.sort()
            
        # Scale atps
        n = self.len()   # number of qualified players
        self.scale(n)

    def derive_data(self, profiles):
        """Aggregates specified-statistic (entry) of profiles into this pack; the aggregated data taking on a form more primed 
        for future data-processing.
        
        Args:
            profiles (dict): all player profiles (contatins all specified-statistic (entry) profiles).
        """
        
        # Extract/Cache specified data
        cached_profiles = {}
        for name in profiles:
            cached_profiles[name] = profiles[name][self.get_key()]
        
        # Repackage specified data
        self.repackage(cached_profiles)
                
    def scale(self, n, stat_param_key01, stat_param_key02=""):
        """Relatively scales player-specific frequencies for a specified-statistic across a scale callibrated to the context
        of other players' respective frequencies for that specified-statistic.

        Args:
            n (int): number of qualified players.
            stat_param_key01 (str): parameter for specified-statistic.
            stat_param_key02 (str, optional): parameter for specified-statistic.
        """
        stat_data = self.get_data(stat_param_key01, stat_param_key02)
        
        # Count out null frequencies
        i = 0
        while i < n and stat_data[i][1] == 0.0:
            i += 1    
            
        # Callibrate scale size to only those players which qualify for this statistic (i.e., having non-null frequencies)
        stat_data_points = list(reversed(stat_data[i:]))  # flip remaining to descending for percentile calculation
        m = n - i  # number of qualified players for this statistic
        i = 0
        
        while i < m:
            elem = stat_data_points[i]
            name = elem[0]
            perc = (m - i) / m
            stat_data[i] = (name, perc)
            i += 1            

class TunnelPairsPack(Pack):
    """A repackaging of the tunnel_pairs statistic of profiler.py's outputted profiles dictionary intended 
    for further data-processing.
    
    A tunnel-pair (tp) is expressed by a pairing of two pitch-types (pt) pt_a and pt_b.
    """
           
    def __init__(self, profiles={}):
        """Initializes this tunnel-pair (tp) pack and dervies tp data from given profiles.
        
        Args:
            profiles (dict): all player profiles (contatins all tp profiles).
        """
        self.data = {}
        for pt_a in PITCH_TYPES:
            self.data[pt_a] = {}
            for pt_b in PITCH_TYPES:
                self.data[pt_a][pt_b] = []
        self.derive_data(profiles)
         
    def get_key(self):
        """Returns the key required to access tunnel-pair (tp) data from profiler.py's outputted profiles dictionary.
        
        Returns:
            str: name of the tp statistic within the profiles dictionary.
        """
        return "tunnel_pairs"
        
    def get_data(self, pt_a, pt_b):
        """Retrieves this pack's frequencies for a given tunnel-pair (tp).

        Args:
            pt_a (str): first pitch-type of specified tp.
            pt_b (str): second pitch-type of specified tp.

        Returns:
            list[float]: frequencies of the specified tp.
        """
        return self.data[pt_a][pt_b]
    
    def extract_data(self, tp_profiles, player, pt_a, pt_b):
        """Retrieves the player-specified tunnel-pair (tp) profile's frequency for a given tunnel-pair (tp).

        Args:
            tp_profiles (dict[dict[dict[float]]]): player-keyed (pair-keyed) tp profiles.
            player (str): name of concerned player.
            pt_a (str): first pitch-type of specified tp.
            pt_b (str): second pitch-type of specified tp.

        Returns:
            float: specified-for player tp frequency.
        """
        return tp_profiles[player][pt_a][pt_b]
            
    def len(self):
        """Returns standard-list-length of this pack.

        Returns:
            int: number of qualified players.
        """
        return len(self.data['FF']['FF'])
        
    def sort(self):
        """Sorts tunnel-pair (tp) data.
        """
        for pt_a in PITCH_TYPES:
            for pt_b in PITCH_TYPES:
                super().sort(pt_a, pt_b)
        
    def repackage(self, tp_profiles):
        """Rearranges player-keyed (pair-keyed) tunnel-pair (tp) dictionaries into a pair-keyed (player-tupled) tp dictionary.

        Args:
            tp_profiles (dict[dict[dict[float]]]): tp profiles.
        """
        for pt_a in PITCH_TYPES:
            for pt_b in PITCH_TYPES: 
                super().repackage(tp_profiles, pt_a, pt_b)
        
    def scale(self, n):
        """Relatively scales player-specific tunnel-pair (tp) frequencies across a scale callibrated to the context of other 
        players' respective tp frequencies.

        Args:
            n (int): number of qualified players.
        """
        for pt_a in PITCH_TYPES:
            for pt_b in PITCH_TYPES:
                super().scale(n, pt_a, pt_b)

class AggregateTunnelPairsPack(Pack):
    """A repackaging of the aggregate_tunnel_pairs statistic of profiler.py's outputted profiles dictionary intended 
    for further data-processing.
    """
           
    def __init__(self, profiles={}):
        """Initializes this aggregate-tunnel-pair (atp) pack and dervies atp data from given profiles.
        
        Args:
            profiles (dict): all player profiles (contatins all atp profiles).
        """
        self.data = {
            'A': [],
            'F-F': [],
            'F-B': [],
            'F-O': [],
            'B-O': []
        }
        self.derive_data(profiles)
         
    def get_key(self):
        """Returns the key required to access aggregate-tunnel-pair (atp) data from profiler.py's outputted profiles dictionary.
        
        Returns:
            str: name of the atp statistic within the profiles dictionary.
        """
        return "aggregate_tunnel_pairs"
        
    def get_data(self, atp, opt=None):
        """Retrieves this pack's frequencies for a given aggregate-tunnel-pair (atp).

        Args:
            atp (str): specified atp.
            opt (None, optional): placeholder to standardize to sibling-class' argumentative-requirements for same method (to avoid TypeError).

        Returns:
            list[float]: frequencies of the specified atp.
        """
        return self.data[atp]
    
    def extract_data(self, atp_profiles, player, atp, opt=None):
        """Retrieves the given aggregate-tunnel-pair (atp) profile's frequency for a given player and aggregate-tunnel-pair (atp).

        Args:
            atp_profiles (dict[dict[float]]): player-keyed (pair-keyed) atp profiles.
            player (str): name of concerned player.
            atp (str): specified atp.
            opt (None, optional): placeholder to standardize to sibling-class' argumentative-requirements for same method (to avoid TypeError).

        Returns:
            float: specified-for player atp frequency.
        """
        return atp_profiles[player][atp]
            
    def len(self):
        """Returns standard-list-length of this pack.

        Returns:
            int: number of qualified players.
        """
        return len(self.data['F-F'])
        
    def sort(self):
        """Sorts aggregate-tunnel-pair (atp) data.
        """
        for atp in self.data:
            super().sort(atp)
        
    def repackage(self, atp_profiles):
        """Rearranges player-keyed (pair-keyed) aggregate-tunnel-pair (atp) dictionaries into a pair-keyed (player-tupled) atp dictionary.

        Args:
            atp_profiles (dict[dict[float]]): atp profiles.
        """
        for atp in self.data:
            super().repackage(atp_profiles, atp)
        
    def scale(self, n):
        """Relatively scales player-specific aggregate-tunnel-pair (atp) frequencies across a scale callibrated to the context of other 
        players' respective atp frequencies.

        Args:
            n (int): number of qualified players.
        """
        for atp in self.data:
            super().scale(n, atp)

# TODO: refactor appropriately...
class ZoneRatesPack(Pack):
    """A repackaging of the aggregate_tunnel_pairs statistic of profiler.py's outputted profiles dictionary intended 
    for further data-processing.
    """
           
    def __init__(self, profiles={}):
        """Initializes this aggregate-tunnel-pair (atp) pack and dervies atp data from given profiles.
        
        Args:
            profiles (dict): all player profiles (contatins all atp profiles).
        """
        self.data = {
            'F-F': [],
            'F-B': [],
            'F-O': [],
            'B-O': []
        }
        self.derive_data(profiles)
         
    def get_key(self):
        """Returns the key required to access aggregate-tunnel-pair (atp) data from profiler.py's outputted profiles dictionary.
        
        Returns:
            str: name of the atp statistic within the profiles dictionary.
        """
        return "aggregate_tunnel_pairs"
        
    def get_data(self, atp, opt=None):
        """Retrieves this pack's frequencies for a given aggregate-tunnel-pair (atp).

        Args:
            atp (str): specified atp.
            opt (None, optional): placeholder to standardize to sibling-class' argumentative-requirements for same method (to avoid TypeError).

        Returns:
            list[float]: frequencies of the specified atp.
        """
        return self.data[atp]
    
    def extract_data(self, atp_profiles, player, atp, opt=None):
        """Retrieves the given aggregate-tunnel-pair (atp) profile's frequency for a given player and aggregate-tunnel-pair (atp).

        Args:
            atp_profiles (dict[dict[float]]): player-keyed (pair-keyed) atp profiles.
            player (str): name of concerned player.
            atp (str): specified atp.
            opt (None, optional): placeholder to standardize to sibling-class' argumentative-requirements for same method (to avoid TypeError).

        Returns:
            float: specified-for player atp frequency.
        """
        return atp_profiles[player][atp]
            
    def len(self):
        """Returns standard-list-length of this pack.

        Returns:
            int: number of qualified players.
        """
        return len(self.data['F-F'])
        
    def sort(self):
        """Sorts aggregate-tunnel-pair (atp) data.
        """
        for atp in self.data:
            super().sort(atp)
        
    def repackage(self, atp_profiles):
        """Rearranges player-keyed (pair-keyed) aggregate-tunnel-pair (atp) dictionaries into a pair-keyed (player-tupled) atp dictionary.

        Args:
            atp_profiles (dict[dict[float]]): atp profiles.
        """
        for atp in self.data:
            super().repackage(atp_profiles, atp)
        
    def scale(self, n):
        """Relatively scales player-specific aggregate-tunnel-pair (atp) frequencies across a scale callibrated to the context of other 
        players' respective atp frequencies.

        Args:
            n (int): number of qualified players.
        """
        for atp in self.data:
            super().scale(n, atp)

def main():
    with open("profiles.pkl", "rb") as f:
        profiles = pickle.load(f)
        
    tp_pack = TunnelPairsPack(profiles)
    tp_pack.percentalize()
    tp_pack.show()     
    
    print("\n\n\n\n\n")   

    atp_pack = AggregateTunnelPairsPack(profiles)
    atp_pack.percentalize()
    atp_pack.show()

if __name__ == "__main__":
    main()