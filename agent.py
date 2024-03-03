
import math
class Agent:
    def __init__(self, x, y, theta, color, noise_linear, noise_angular, noise_measurement):
        self.pose_x = x
        self.pose_y = y
        self.pose_theta = theta
        self.color = color
        self.weight = 0.0
        self.noise_linear = noise_linear
        self.noise_angular = noise_angular
        self.noise_measurement = noise_measurement

    #this function moves the agent
    def move(self, dist, rot, width, height):
        angle = self.pose_theta + self.noise_angular
        angle = self.normalize_angle_radians(angle)
        #compute new poses
        new_pose_x = self.pose_x + (dist * math.cos(angle) + self.noise_linear)
        new_pose_y = self.pose_y + (dist * math.sin(angle) + self.noise_linear)

        #check boundaries
        if new_pose_x > width:
            new_pose_x = 0
        elif new_pose_x < 0:
            new_pose_x = width
        
        if new_pose_y > height:
            new_pose_y = 0
        elif new_pose_y < 0:
            new_pose_y = height
        
        #update agent's pose
        self.pose_x = new_pose_x
        self.pose_y = new_pose_y
        self.pose_theta += rot

    def observe(self, landmarks):
        distances = []
        for landmark in landmarks:
            land_x, land_y = landmark    
            distances.append((math.sqrt((land_x - self.pose_x)**2 + (land_y - self.pose_y)**2) + self.noise_measurement))
        return distances
        
    def normalize_angle_radians(self, angle):
        # Ensure the angle is within the range [-180, 180]
        normalized_angle = angle % (2 * math.pi)

        if normalized_angle > math.pi:
            normalized_angle -= 2 * math.pi

        return normalized_angle
