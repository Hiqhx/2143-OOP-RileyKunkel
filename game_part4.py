import random

class Dice(object):
    """
    @Class: Dice
    @Description: 
        Represents a single "die" with X number of sides.
    @Methods:
        Roll - Rolls the dice and returns a value between 1 and "number of sides" 
    """
    def __init__(self,num_sides=6):
        self.NumSides = num_sides

    def Roll(self):
        return random.randint(1,self.NumSides)



class PigDice(object):
    """
    @Class: PigDice
    @Description: 
        Represents the game of pig (dice game)
    @Methods:
        Roll - Rolls the "die" or "dice" and returns a list of rolled values
    """
    def __init__(self,num_dice=1,dice_sides=6,skunk_value=1):
        self.NumDice = num_dice
        self.DiceSides = dice_sides
        self.DiceList = []
        self.SkunkValue = skunk_value
        for i in range(self.NumDice):
            self.DiceList.append(Dice(self.DiceSides))

    def Roll(self):
        """
        @Method: Roll
        @Description: 
            One roll in a pig game, with 1 to NumDice per roll
        @Returns: int: [0=skunk value occured, total of all dice otherwise]
        """ 
        scores = []
        for d in self.DiceList:
            scores.append(d.Roll())
            if self.SkunkValue in scores:
                return 0 
        return sum(scores)
  
  

class LeaderBoard(object):
    """
    @Class: LeaderBoard
    @Description: 
        A global list of all players
    @Methods:
        
    """
    __shared_state = {}

    def __init__(self,player=None):
        self.__dict__ = self.__shared_state

        if len(self.__shared_state.keys()) == 0:
          self.players = {}
          
        if not player is None:
            self.players[player.name] = player


    def __str__(self):
      s = ''
      for name,p in self.players.items():
        s += p.__str__()
        s += ',\n'
      
      return s
      
    def Find(self,name,key):
      """
      @Method: Find
      @Description: 
          Retreive a key value from player.
          e.g. score = leaderboard.Find('Bob','Score)
               total_rolls = leaderbard.Find('Sue','tot_rolls')
      @Returns: Mixed (whatever type the value is from the player)
      """ 
      if not name in self.players:
        return None
      else:
          return self.players[name][key]
      
      return None
 


class Player(object):
  """
  @Class: Player
  @Description: 
      Represents a single player for our pig game
  @Methods:
      
  """
  def __init__(self,name=None,strategy=1):
    self.name = name
    self.score = 0
    self.tot_rolls = 0   
    self.round_score = 0
    self.round_rolls = 0
    self.leaderBoard = LeaderBoard(self)
    self.dice = PigDice()
    self.strategy = strategy
    if self.strategy is 1: #Basic
        self.targetscore = random.randint(18,24)
        self.targetrolls = random.randint(6,8)
    if self.strategy is 2: #Aggressive
        self.targetscore = random.randint(28,33)
        self.targetrolls = random.randint(8,12)
    elif self.strategy is 3: #Cautious
        self.targetscore = random.randint(10,16)
        self.targetrolls = random.randint(3,6)
    elif self.strategy is 4: #SprintToFinish
        if self.score / 100 >= .75:
            while self.score+self.round_score<100:
                self.Roll()
        else:
            self.targetscore = random.randint(10,16)
            self.targetrolls = random.randint(3,6)
            

  def Roll(self):
      roll = self.dice.Roll()
      self.round_score += roll
      self.round_rolls += 1
      return roll

    
  def NewGame(self):
    self.round_score = 0
    self.round_rolls = 0
    self.score = 0
    self.tot_rolls = 0
    
    
  def __str__(self):
    return "[Name:%s, Score:%d, Tr:%s, Rs:%s, Rr:%s, Strat:%s]" % (self.name,self.score,self.tot_rolls,self.round_score,self.round_rolls,self.strategy)
    
  def __getitem__(self, key):
      if hasattr(self, key):
          return getattr(self, key)
      else:
          return None
 


"""
This Class represents one instance of a game with X players rolling X dice playing to a score of X.
"""
class PigGame(object):
    """
    @Method: Init
    @Description: Initializes a pig game instance
    @Params:
        list: Players - A list of player names
        int: NumDice - Number of dice per roll
        int: RandomRolls - Top value of random range for rolls
        int: TargetScore - Target score to trigger a winner
    @Returns: None
    """
    def __init__(self, **kwargs): 
        self.Players = []
        self.NumDice = kwargs['num_dice']
        self.RandomRollsMax = kwargs['random_roles']
        self.TargetScore = kwargs['target_score']
        self.WinnerName = None
        self.GameRounds = 0

        
        # initialize all players
        self.AddPlayers(kwargs['players'])
            
        
        
    def __str__(self):
        string = ""
        for obj in self.Players:
            string += obj.__str__() + "\n"
        return string
        

    def AddPlayers(self,players):
        """
        @Method: AddPlayers
        @Description: Adds a new player or players to the game
            Example: {
                       'bob':<player_object>
                       'sue':<player_object>
                     }
        @Params: [] - players
        @Returns: None
        """
        if not type(players) == list:
            self.Players.append(players)
        else:
            for p in players:
                self.Players.append(p)
                    
     
    def RunGame(self):
        """
        @Method: WinnerExists
        @Description: Checks to see if a player has acheived the target score.
        @Params:None
        @Returns: bool
        """    
        
        # Main game loop
        self.GameRounds = 0
        while not self.WinnerExists():
            for PlayerObj in self.Players:
                r=PlayerObj.Roll()
                while (PlayerObj.targetrolls>PlayerObj.round_rolls or PlayerObj.targetscore>PlayerObj.round_score):
                    if r is 0 and PlayerObj.score+PlayerObj.round_score<100:
                      break
                    r=PlayerObj.Roll()
                PlayerObj.score+=PlayerObj.round_score
                PlayerObj.tot_rolls+=PlayerObj.round_rolls
            self.GameRounds += 1
        


    def WinnerExists(self):
        """
        @Method: WinnerExists
        @Description: Checks to see if a player has acheived the target score.
        @Params:None
        @Returns: bool
        """
        for p in self.Players:
          if p.score >= self.TargetScore:
            return True
        return False
        
    def NewGame(self):
      for p in self.Players:
        p.NewGame()


    def Winner(self):
        """
        @Method: Winner
        @Description: Returns the winner, if there is one.
        @Params:None
        @Returns: [string,None]: Players name or None
        """        
        for p in self.Players:
          if p.score >= self.TargetScore:
            return p.name 
        
        return None
 


players = [Player('Bob',1),Player('Sue',2),Player('Dax',3),Player('Ann',4)]

kwargs = {'num_dice':1,'random_roles':6,'target_score':100,'players':players}
pg = PigGame(**kwargs)

Winners = {}

runs = 1000
P = PigGame(**kwargs)
for i in range(runs):
  P.RunGame()
  winner = P.Winner()
  if not winner in Winners:
    Winners[winner] = []
  Winners[winner].append(P.GameRounds)
  P.NewGame()

for winner,wins in Winners.items():
  print(winner,len(wins),sum(wins)/len(wins))
  
