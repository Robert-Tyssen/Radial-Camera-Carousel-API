from rest_framework import serializers

# Serializer class to ensure that analysis submissions are sent in the correct format
class AnalysisSubmissionSerializer(serializers.Serializer):
  def validate(self, data):
    if not isinstance(data, dict):
      raise serializers.ValidationError("Payload must be a dictionary.")

    seen_keys = set()

    validated_data: dict[int, list[int]] = {}

    for key, value in self.initial_data.items():
      # Ensure keys are integers
      if not isinstance(key, int) and not key.isdigit():
        raise serializers.ValidationError(f"Key '{key}' must be an integer.")
            
      key = int(key)  # Convert string keys to integers

      # Ensure key is ≤ 15
      if key > 15 or key < 0:
        raise serializers.ValidationError(f"Key '{key}' must be between 0-15.")

      # Ensure no duplicate keys
      if key in seen_keys:
        raise serializers.ValidationError(f"Duplicate key found: {key}")
        
      seen_keys.add(key)

      # Ensure values are lists of integers
      if not isinstance(value, list):
        raise serializers.ValidationError(f"Value for key '{key}' must be a list.")
      
      # Ensure list is not empty
      if len(value) == 0:
        raise serializers.ValidationError(f"Value for key '{key}' must not be empty.")
      
      validated_data[key] = []

      seen_values = set()
      for item in value:
        if not isinstance(item, int):
          raise serializers.ValidationError(f"Value '{item}' in key '{key}' must be an integer.")
                
        if item > 7 or item < 0:
          raise serializers.ValidationError(f"Value '{item}' in key '{key}' must be between 0-7")

        if item in seen_values:
          raise serializers.ValidationError(f"Duplicate value '{item}' found in list for key '{key}'.")
          
        seen_values.add(item)
        validated_data[key].append(item)


    return validated_data