from Minecraft_env import MinecraftEnv
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback

def test(total_timesteps):
    env = MinecraftEnv(verbose=True) 
    loaded_model = PPO.load("./policy_checkpoints/policy_14000_steps.zip")
    observation = env.reset()
    for step in range(total_timesteps):
        action, _ = loaded_model.predict(observation, deterministic=True)
        observation, reward, done, _ = env.step(action)
        print("reward",reward)
        print(action)
        if done:
            break
    env.close()
    

def train(model_number, load_pretrained=False):
    env = MinecraftEnv()
    if load_pretrained:
        model =  PPO.load("./policy_checkpoints/model"+str(model_number)+ "/policy_14000_steps.zip")
    else:
        model = PPO("MultiInputPolicy", env, verbose=1, learning_rate=0.75, tensorboard_log="./policy_checkpoints/model"+str(model_number))

    checkpoint_callback = CheckpointCallback(save_freq=1000, save_path="./policy_checkpoints/model"+str(model_number), name_prefix="policy")

    model.learn(total_timesteps=1000000, callback=[checkpoint_callback]) 

    model.save("final_policy")
    
    env.close()
  

if __name__ == "__main__" :
    model_number = 1 
    mode = "train"
    load_pretrained=True
    total_timesteps = 500
    if mode ==  "test":
        test(total_timesteps)
    
    else:
        train(model_number,load_pretrained = load_pretrained)
        
