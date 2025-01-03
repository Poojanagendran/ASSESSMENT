import hashlib

file = "https://s3-ap-southeast-1.amazonaws.com/all-hirepro-files/crpoqa/common/ed2ccbaa-6f9d-4099-96cc-0b4b18b63ce9inputTestCase.txt"
# file2 = "https://s3-ap-southeast-1.amazonaws.com/test-all-hirepro-files/AT/CodingQuestionAttachment/130490/96b107ab-cfce-4cea-86ae-9b38e74532b6inputText253321.txt"
hash = hashlib.md5(str(file).encode()).hexdigest()
print("coding_question_attachment:" + hash)