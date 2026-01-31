# voicecore/features/base_feature.py
class BaseFeature:
    def handle_text(self, text: str):
        """Process recognized text and perform an action."""
        raise NotImplementedError
    
    def handle_partial(self, text: str):
        """Process recognized partial text and perform an action."""
        raise NotImplementedError