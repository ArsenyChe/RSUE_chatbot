import json

class JSONFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_intents(self):
        with open(self.file_path, "r", encoding='utf-8') as file:
            intents_data = json.load(file)
        return intents_data.get('intents', [])
    
    def save_intents(self, intents):
        intents_data = {"intents": intents}
        with open(self.file_path, 'w') as file:
            json.dump(intents_data, file, indent=4)
    
    def add_intent(self, tag):
        intents = self.load_intents()
        tag_check = any(intent["tag"] == tag for intent in intents)
        if not tag_check:
            new_intent = {"tag": tag, "patterns": [], "responses": []}
            intents.append(new_intent)
            self.save_intents(intents)
            return f"Тег '{tag}' добавлен"
        else: return f"Тег '{tag}' уже существует"
    
    def delete_intent(self, tag):
        intents = self.load_intents()
        tag_check = any(intent["tag"] == tag for intent in intents)
        if tag_check:
            intents = [intent for intent in intents if intent["tag"] != tag]
            self.save_intents(intents)
            return f"Тег '{tag}' удален"
        else: return f"Тег '{tag}' отсутствует"
    
    def edit_intent(self, tag, new_tag):
        intents = self.load_intents()
        tag_check = any(intent["tag"] == tag for intent in intents)
        new_tag_check = any(intent["tag"] == new_tag for intent in intents)
        if tag_check and not new_tag_check:
            [intent.update({"tag": new_tag}) if intent.get("tag") == tag else intent for intent in intents]
            self.save_intents(intents)
            return f"Тег '{tag}' изменен на '{new_tag}'"
        else: return f"Тег '{tag}' отсутствует или '{new_tag}' совпадает с существующими тегами"

    def add_pattern(self, tag, pattern):
        intents = self.load_intents()
        tag_pattern = any(pattern in intent["patterns"] for intent in intents)
        if not tag_pattern:
            [intent["patterns"].append(pattern) if intent.get("tag") == tag else intent for intent in intents]
            self.save_intents(intents)
            return f"'{pattern}' добавлен"
        else: return f"'{pattern}' уже существует"

    def delete_pattern(self, tag, pattern):
        intents = self.load_intents()
        tag_pattern = any(pattern in intent["patterns"] for intent in intents)
        if tag_pattern:
            [intent['patterns'].remove(pattern) for intent in intents if intent['tag'] == tag and pattern in intent['patterns']]
            self.save_intents(intents)
            return f"'{pattern}' удален"
        else: return f"'{pattern}' отсутствует"

    def add_response(self, tag, response):
        intents = self.load_intents()
        tag_response = any(response in intent["responses"] for intent in intents)
        if not tag_response:
            [intent["responses"].append(response) if intent.get("tag") == tag else intent for intent in intents]
            self.save_intents(intents)
            return f"'{response}' добавлен"
        else: return f"'{response}' уже существует"

    def delete_response(self, tag, response):
        intents = self.load_intents()
        tag_response = any(response in intent["responses"] for intent in intents)
        if tag_response:
            [intent['responses'].remove(response) for intent in intents if intent['tag'] == tag and response in intent['responses']]
            self.save_intents(intents)
            return f"'{response}' удален"
        else: return f"'{response}' отсутствует"
    
    def display_intents(self):
        intents = self.load_intents()
        for intent in intents:
            print(f'Tag: {intent["tag"]}')
            print(f'Patterns: {intent["patterns"]}')
            print(f'Responses: {intent["responses"]}')
            print()

    def show_tags(self):
        intents = self.load_intents()
        tags: list[str]=[]
        for intent in intents:
            tags.append(intent["tag"])
        return '\n'.join(map(str, tags))
    
    def show_patterns(self, tag):
        intents = self.load_intents()
        tag_check = any(intent["tag"] == tag for intent in intents)
        if tag_check:
            patterns = ([intent["patterns"] for intent in intents if intent["tag"] == tag and intent["patterns"] != ""])
            if len(patterns) == 0:
                return f"Для тега '{tag}' отсутствуют шаблоны"
            flat_patterns = sum(patterns, [])
            return '\n'.join(map(str, flat_patterns))
        else: return f"Тег '{tag}' отсутствует"
    
    def show_responses(self, tag):
        intents = self.load_intents()
        tag_check = any(intent["tag"] == tag for intent in intents)
        if tag_check:
            responses = ([intent["responses"] for intent in intents if intent["tag"] == tag and intent["responses"] != ""])
            if len(responses) == 0:
                return f"Для тега '{tag}' отсутствуют ответы"
            flat_responses = sum(responses, [])
            return '\n'.join(map(str, flat_responses))
        else: return f"Тег '{tag}' отсутствует"