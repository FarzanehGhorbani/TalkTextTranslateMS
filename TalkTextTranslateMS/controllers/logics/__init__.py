# import argostranslate.package
# import argostranslate.translate

# class Translator:
#     def __init__(self, from_code, to_code):
#         self.from_code = from_code
#         self.to_code = to_code
#         self.translation = None

#     def setup_translation(self):
#         argostranslate.package.update_package_index()
#         available_packages = argostranslate.package.get_available_packages()
#         package = next((p for p in available_packages if p.from_code == self.from_code and p.to_code == self.to_code), None)
#         if package:
#             download_path = package.download()
#             argostranslate.package.install_from_path(download_path)

#     def load_translation(self):
#         installed_languages = argostranslate.translate.get_installed_languages()
#         from_lang = next((lang for lang in installed_languages if lang.code == self.from_code), None)
#         to_lang = next((lang for lang in installed_languages if lang.code == self.to_code), None)
#         if from_lang and to_lang:
#             self.translation = from_lang.get_translation(to_lang)

#     def translate(self, text):
#         if self.translation:
#             return self.translation.translate(text)
#         else:
#             return None

# # Example usage:
# translator = Translator(from_code="en", to_code="fa")
# translator.setup_translation()
# translator.load_translation()
# translated_text = translator.translate("Hello World!")
# translated_text = translator.translate("Hi!")

# if translated_text:
#     print(f"Translated Text: {translated_text}")
# else:
#     print("Translation failed.")
