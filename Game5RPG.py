import random, time, os

def clear(): os.system('cls' if os.name=='nt' else 'clear')
def sp(t): 
    for c in t: print(c,end='',flush=True); time.sleep(0.02)
    print()

class Character:
    def __init__(self,name,hp,atk,dfn):
        self.name=name; self.max_hp=hp; self.hp=hp; self.atk=atk; self.dfn=dfn
    def alive(self): return self.hp>0
    def take_dmg(self,d):
        a=max(1,d-self.dfn); self.hp=max(0,self.hp-a); return a
    def bar(self):
        f=int(self.hp/self.max_hp*20)
        return f"[{'█'*f}{'░'*(20-f)}] {self.hp}/{self.max_hp}"

class Player(Character):
    def __init__(self,name,cls):
        stats={"Warrior":(120,18,8),"Mage":(80,25,3),"Rogue":(95,20,5)}
        hp,atk,dfn=stats[cls]
        super().__init__(name,hp,atk,dfn)
        self.cls=cls; self.level=1; self.xp=0; self.xp_next=30
        self.gold=10; self.potions=2; self.special_used=False
    def special(self,enemy):
        if self.cls=="Warrior": dmg=self.atk*2; sp(f"  Shield Bash! {enemy.take_dmg(dmg)} dmg!")
        elif self.cls=="Mage":  dmg=self.atk*2+random.randint(5,15); sp(f"  Fireball! {enemy.take_dmg(dmg)} dmg!")
        else:                   dmg=self.atk*3; sp(f"  Backstab! {enemy.take_dmg(dmg)} dmg!")
        self.special_used=True
    def gain_xp(self,x):
        self.xp+=x
        if self.xp>=self.xp_next:
            self.level+=1; self.xp-=self.xp_next; self.xp_next=int(self.xp_next*1.5)
            self.max_hp+=15; self.hp=min(self.hp+15,self.max_hp); self.atk+=3; self.dfn+=1
            sp(f"  LEVEL UP! Now level {self.level}! HP+15 ATK+3 DEF+1")
    def potion(self):
        if self.potions>0:
            h=min(30,self.max_hp-self.hp); self.hp+=h; self.potions-=1
            sp(f"  Healed {h} HP. Potions left: {self.potions}")
        else: sp("  No potions!")

ENEMIES=[("Goblin",30,8,1,10,5,"👺"),("Skeleton",45,12,3,18,8,"💀"),
         ("Orc",70,16,6,30,15,"🧌"),("Dark Mage",55,22,2,35,20,"🧙"),("Dragon",120,28,10,80,50,"🐉")]

def spawn(level):
    t=random.choice(ENEMIES[:min(level+1,len(ENEMIES))])
    s=1+(level-1)*0.15
    e=Character(t[0],int(t[1]*s),int(t[2]*s),t[3])
    e.xp_reward=t[4]; e.gold_reward=t[5]; e.emoji=t[6]; e.max_hp=e.hp
    e.bar=lambda: f"[{'█'*int(e.hp/e.max_hp*20)}{'░'*(20-int(e.hp/e.max_hp*20))}] {e.hp}/{e.max_hp}"
    return e

def battle(p,e):
    sp(f"\n  A wild {e.emoji} {e.name} appears!")
    p.special_used=False
    while p.alive() and e.alive():
        print(f"\n  {e.emoji} {e.name}: {e.bar()}")
        print(f"  You (Lv{p.level}): {p.bar()}")
        print(f"  Gold:{p.gold} Potions:{p.potions} XP:{p.xp}/{p.xp_next}")
        print("  [1]Attack [2]Special(once) [3]Potion [4]Flee")
        c=input("  > ").strip()
        if c=="1":
            d=p.atk+random.randint(-2,5); sp(f"  You attack for {e.take_dmg(d)} dmg!")
        elif c=="2":
            if not p.special_used: p.special(e)
            else: sp("  Already used!"); continue
        elif c=="3": p.potion()
        elif c=="4":
            if random.random()<0.4: sp("  You fled!"); return "fled"
            else: sp("  Can't escape!")
        else: continue
        if e.alive():
            d=e.atk+random.randint(-3,3); sp(f"  {e.name} attacks for {p.take_dmg(d)} dmg!")
    if p.alive():
        sp(f"  Victory! +{e.xp_reward}XP +{e.gold_reward}gold")
        p.gain_xp(e.xp_reward); p.gold+=e.gold_reward; return "win"
    return "lose"

print("="*40+"\n  DUNGEON OF CODE\n"+"="*40)
name=input("  Hero name: ").strip() or "Hero"
print("  [1]Warrior [2]Mage [3]Rogue")
cls={"1":"Warrior","2":"Mage","3":"Rogue"}.get(input("  > ").strip(),"Warrior")
p=Player(name,cls); wins=0
sp(f"\n  Welcome, {name} the {cls}!")

while p.alive():
    if wins>0 and wins%3==0:
        print(f"\n  SHOP — Gold:{p.gold}\n  [1]Potion(15g) [2]Leave")
        if input("  > ")=="1":
            if p.gold>=15: p.gold-=15; p.potions+=1; sp("  Bought a potion!")
            else: sp("  Not enough gold!")
    e=spawn(p.level)
    r=battle(p,e)
    if r=="win": wins+=1; sp(f"  Enemies defeated: {wins}")
    elif r=="lose": break

if not p.alive():
    print(f"\n  {name} has fallen.\n  Level:{p.level} Gold:{p.gold} Wins:{wins}")

input("\nPress Enter to exit...")