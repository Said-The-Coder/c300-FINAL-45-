from controller import Robot

bot = Robot()

timestep = 64

cam=bot.getDevice('camera')

left_wheel = bot.getDevice('left_front_wheel')
right_wheel = bot.getDevice('right_front_wheel')
l_steer = bot.getDevice('left_steer')
r_steer = bot.getDevice('right_steer')

# enable the camera
cam.enable(timestep)
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))
l_steer.setPosition(0)
r_steer.setPosition(0)
left_wheel.setVelocity(0)
right_wheel.setVelocity(0)

lidar=bot.getDevice('Sick LMS 291')
lidar.enable(timestep)
lidar.enablePointCloud()

def wait(time_steps):
    time_counter=0
    while bot.step(timestep) != -1:
        if(time_counter>=time_steps):
            break
        time_counter+=1

while bot.step(timestep) != -1:
    val=lidar.getRangeImage()
    print(val)
    affected_rays=val[85:96]
    obstacle_detected=any([value<5 for value in affected_rays])
    print(obstacle_detected)
    
    img=cam.getImage()
    image_width=cam.getWidth()
    image_height=cam.getHeight()
    
    x_yellow=[]
    for x in range(0,image_width):
        for y in range(0,image_height):
        
            red_val=cam.imageGetRed(img,image_width,x,y)
            green_val=cam.imageGetGreen(img,image_width,x,y)
            blue_val=cam.imageGetBlue(img,image_width,x,y)
            
            if(red_val>190 and green_val>180 and blue_val>90):
                x_yellow.append(x)
                
    if(x_yellow):
        x_total=0
        for x in x_yellow:
            x_total=x_total+x
        x_average=x_total/len(x_yellow)
    x_center=image_width/2
    
    if(obstacle_detected):
        l_steer.setPosition(-0.7)
        r_steer.setPosition(-0.7)
        wait(10)
        
        l_steer.setPosition(0)
        r_steer.setPosition(0)
        wait(10)
        
        l_steer.setPosition(0.7)
        r_steer.setPosition(0.7)
        wait(10)
    
    if(x_average<x_center):
        l_steer.setPosition(-0.1)
        r_steer.setPosition(-0.1)
        
    elif(x_average>x_center):
        l_steer.setPosition(0.1)
        r_steer.setPosition(0.1)
        
    left_wheel.setVelocity(10)
    right_wheel.setVelocity(10)
            
