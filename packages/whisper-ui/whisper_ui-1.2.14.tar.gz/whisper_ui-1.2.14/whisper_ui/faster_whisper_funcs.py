import torch
import whisperx

from whisper_ui.whisper_funcs import *

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class WhisperXInterface(ModelInterface):
    
    def __init__(self):
        super().__init__()
    
    def get_model(self, switch_model: bool = False):
        
        model_name = USER_PREFS["model"]
        
        if not check_model(model_name):
            print(f'\tWarning: model {model_name} not found in cache. Please download it.')
            return
        
        if self.model is None or switch_model:
            print(f'\tLoading model {model_name}. This may take a while if you have never used this model.')
            print(f'\t\tChecking for GPU...')
            device = 'cuda' if is_available() else 'cpu'
            if device == 'cuda':
                print('\t\tGPU found.')
            else:
                print('\t\tNo GPU found. Using CPU.')
            try:
                self.model = whisperx.load_model(name=USER_PREFS['model'], device=device, in_memory=True)
            except:
                try:
                    self.model = whisper.load_model(name=USER_PREFS['model'], device=device)
                except:
                    print('\t\tWarning: issue loading model onto GPU. Using CPU.')
                    self.model = whisper.load_model(name=USER_PREFS['model'], device='cpu')
            print(f'\tLoaded model {model_name} successfully.')
        else:
            print(f'\tUsing currently loaded model ({model_name}).')
            
        self.model.eval()