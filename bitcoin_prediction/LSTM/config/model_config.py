# config/model_config.py

class ModelConfig:
    # Data parameters
    TIME_STEPS = 30  # Number of days to look back
    TRAIN_SPLIT = 0.8  # Training/testing split ratio
    
    # LSTM model parameters
    MODEL_PARAMS = {
        'input_shape': None,  # Will be set during runtime
        'units': [128, 64],  # Number of units in each LSTM layer
        'dropout': 0.3,
        'activation': 'tanh',
        'recurrent_activation': 'sigmoid'
    }
    
    # Training parameters
    TRAINING_PARAMS = {
        'epochs': 100,
        'batch_size': 64,
        'learning_rate': 0.001,
        'validation_split': 0.2
    }
    
    # File paths
    MODEL_PATH = '../models/lstm_model.h5'