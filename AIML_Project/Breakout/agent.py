import random

pre_loc = None
direction = (0,0)

def decide(instr):
    global pre_loc
    global direction

    #if (len(instr) <= 6):
     #   return 0

    infor = str(instr)
    infor_list = infor.split(' ')
    
    dire = 0
    paddle_y = 555
    paddle_x = int(infor_list[2])
    paddle_width = int(infor_list[3])
    ball_x = int(infor_list[0][2:])
    ball_y = int(infor_list[1])

    if (pre_loc == None) :
        pre_loc = (ball_x, ball_y)
    else:
        direction = (ball_x - pre_loc[0], ball_y - pre_loc [1])
        pre_loc = None
    if (direction[1] > 0): #downward
        predict_bx = ball_x + ((paddle_y - ball_y)/direction[1])*direction[0]
        predict_px = paddle_x 
        if predict_bx > predict_px:
            dire = 1
        elif predict_bx < predict_px:
            dire = -1
    else: #upward
        if ball_x > paddle_x:
            dire = 1
        elif ball_x < paddle_x:
            dire = -1
    if (paddle_width >= 25): #paddle stop
        if(ball_y > paddle_y - 3*direction[1]):
            dire = 0
    else: 
        if(ball_y > paddle_y - 2.5*direction[1]):
            p = random.random()
            if p < 0.25:
                dire = -1
            elif p < 0.5:
                dire = 1
            else:
                dire = 0
    return dire
