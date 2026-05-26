import os, random, time, sys

try:
    import msvcrt
    def get_key():
        if msvcrt.kbhit():
            k = msvcrt.getch()
            if k == b'\xe0':
                k = msvcrt.getch()
                return {b'H':'UP',b'P':'DOWN',b'K':'LEFT',b'M':'RIGHT'}.get(k)
            return k.decode('utf-8','ignore').upper()
    CLEAR = 'cls'
except ImportError:
    import tty, termios, select
    def get_key():
        if select.select([sys.stdin],[],[],0)[0]:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            termios.tcsetattr(sys.stdin,termios.TCSADRAIN,termios.tcgetattr(sys.stdin))
            if ch == '\x1b':
                ex = sys.stdin.read(2) if select.select([sys.stdin],[],[],0.05)[0] else ''
                return {'[A':'UP','[B':'DOWN','[D':'LEFT','[C':'RIGHT'}.get(ex)
            return ch.upper()
    CLEAR = 'clear'

W, H = 20, 15

def new_game():
    snake = [(W//2,H//2),(W//2-1,H//2),(W//2-2,H//2)]
    return {"snake":snake,"dir":(1,0),"score":0,"food":spawn(snake)}

def spawn(snake):
    while True:
        p = (random.randint(0,W-1),random.randint(0,H-1))
        if p not in snake: return p

def draw(g):
    os.system(CLEAR)
    print(f"SNAKE | Score: {g['score']} | WASD to move | Q to quit")
    print("+" + "-"*W + "+")
    for y in range(H):
        row = "|"
        for x in range(W):
            p=(x,y)
            if p==g["snake"][0]: row+="O"
            elif p in g["snake"]: row+="o"
            elif p==g["food"]: row+="*"
            else: row+=" "
        print(row+"|")
    print("+" + "-"*W + "+")

def update(g):
    hx,hy = g["snake"][0]
    dx,dy = g["dir"]
    head = (hx+dx,hy+dy)
    if not(0<=head[0]<W and 0<=head[1]<H) or head in g["snake"]:
        return False
    g["snake"].insert(0,head)
    if head==g["food"]:
        g["score"]+=10
        g["food"]=spawn(g["snake"])
    else:
        g["snake"].pop()
    return True

MOVES = {'UP':(0,-1),'DOWN':(0,1),'LEFT':(-1,0),'RIGHT':(1,0),'W':(0,-1),'S':(0,1),'A':(-1,0),'D':(1,0)}

print("SNAKE GAME - WASD or Arrow Keys\nPress Enter to start...")
input()
g = new_game()

while True:
    draw(g)
    k = get_key()
    if k=='Q': break
    if k and k in MOVES:
        nd=MOVES[k]
        if (nd[0]+g["dir"][0],nd[1]+g["dir"][1])!=(0,0):
            g["dir"]=nd
    if not update(g):
        draw(g)
        print(f"\nGAME OVER! Score: {g['score']}")
        if input("Play again? (yes/no): ").lower() in ("yes","y"):
            g=new_game()
        else: break
    time.sleep(0.15)