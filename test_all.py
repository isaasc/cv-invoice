import develop
import os


tests = os.listdir('testes')

for test in tests:
    develop.run_tesseract(test)
    # develop.run_easyocr(test)

print()
