# bot.py

from command import Command
from buttons import Buttons
import numpy as np
import tensorflow as tf
import os

class Bot:
    def __init__(self):
        # Try loading the model with error handling
        try:
            if os.path.exists('bot_model.h5'):
                print("Loading model from model.h5")
                self.model = tf.keras.models.load_model('model.h5')
                print("Model loaded successfully!")
                # Print model summary to verify it loaded correctly
                self.model.summary()
            else:
                print("ERROR: model.h5 not found!")
                raise FileNotFoundError("model.h5 not found")
        except Exception as e:
            print(f"CRITICAL ERROR loading model: {e}")
            raise  # Re-raise the exception to stop execution
        
        # Counter to help with debugging
        self.prediction_count = 0
        
    def extract_features(self, game_state, player):
        if player == "1":
            me, opp = game_state.player1, game_state.player2
        else:
            me, opp = game_state.player2, game_state.player1

        features = [
            game_state.timer,
            me.player_id,
            me.health,
            me.x_coord,
            me.y_coord,
            int(me.is_jumping),
            int(me.is_crouching),
            int(me.is_player_in_move),
            me.move_id,
            opp.player_id,
            opp.health,
            opp.x_coord,
            opp.y_coord,
            int(opp.is_jumping),
            int(opp.is_crouching),
            int(opp.is_player_in_move),
            opp.move_id
        ]
        
        return features

    def fight(self, game_state, player):
        cmd = Command()
        
        # Check if round has started
        if not game_state.has_round_started or game_state.is_round_over:
            return cmd
            
        # Extract features for the model
        feats = self.extract_features(game_state, player)
        X = np.array([feats], dtype=np.float32)
        
        # Get predictions from model
        preds = self.model.predict(X, verbose=0)[0]
        
        # Print prediction values occasionally for debugging
        self.prediction_count += 1
        if self.prediction_count % 10 == 0:  # Print every 10th prediction
            print(f"Prediction #{self.prediction_count}")
            print(f"Raw predictions: {preds}")
        
        # Test different thresholds:
        # Using very low threshold (0.1) to see if model outputs ANY signals
        threshold = 0.05
        
        # Create buttons based on predictions with low threshold
        b = Buttons()
        b.up    = bool(preds[0] > threshold)
        b.down  = bool(preds[1] > threshold)
        b.right = bool(preds[2] > threshold)
        b.left  = bool(preds[3] > threshold)
        b.Y     = bool(preds[4] > threshold)
        b.B     = bool(preds[5] > threshold)
        b.X     = bool(preds[6] > threshold)
        b.A     = bool(preds[7] > threshold)
        b.L     = bool(preds[8] > threshold)
        b.R     = bool(preds[9] > threshold)
        
        # Print which buttons are being pressed
        if self.prediction_count % 10 == 0:
            active_buttons = []
            if b.up: active_buttons.append("UP")
            if b.down: active_buttons.append("DOWN")
            if b.right: active_buttons.append("RIGHT")
            if b.left: active_buttons.append("LEFT")
            if b.Y: active_buttons.append("Y")
            if b.B: active_buttons.append("B")
            if b.X: active_buttons.append("X") 
            if b.A: active_buttons.append("A")
            if b.L: active_buttons.append("L")
            if b.R: active_buttons.append("R")
            
            print(f"Active buttons: {', '.join(active_buttons) if active_buttons else 'NONE'}")
        
        cmd.player_buttons = b
        return cmd