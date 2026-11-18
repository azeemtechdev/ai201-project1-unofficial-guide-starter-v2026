# Capstone run: before  (2026-11-17 21:57)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Real timeout gives clear message + error/timeout log row | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every request logged (10 new lines, 1 forced failure) | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 3. Invalid input rejected, 0 tokens, logged | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Warm requests under 1.9s | 9 of 10 | 4/10 | 7/10 | 5/10 | MISSED |
| 5. Original questions still contain expected phrase | 5 of 5 | 2/5 | 2/5 | 1/5 | MISSED |

## 1. Real timeout gives clear message + error/timeout log row

**Trial 1**
```
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
```

**Trial 2**
```
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
```

**Trial 3**
```
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'
```

## 2. Every request logged (10 new lines, 1 forced failure)

**Trial 1**
```
new log lines: 10 (expected 10)
statuses: ['answered', 'answered', 'answered', 'answered', 'error', 'answered', 'answered', 'answered', 'answered', 'answered']
```

**Trial 2**
```
new log lines: 10 (expected 10)
statuses: ['answered', 'answered', 'answered', 'answered', 'error', 'answered', 'answered', 'answered', 'answered', 'answered']
```

**Trial 3**
```
new log lines: 10 (expected 10)
statuses: ['answered', 'answered', 'answered', 'answered', 'error', 'answered', 'answered', 'answered', 'answered', 'answered']
```

## 3. Invalid input rejected, 0 tokens, logged

**Trial 1**
```
PASS len=3 status=rejected tokens=0 msg='Please type a question.'
PASS len=4 status=rejected tokens=0 msg='Please type a question.'
PASS len=501 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
PASS len=800 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
PASS len=2000 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
```

**Trial 2**
```
PASS len=3 status=rejected tokens=0 msg='Please type a question.'
PASS len=4 status=rejected tokens=0 msg='Please type a question.'
PASS len=501 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
PASS len=800 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
PASS len=2000 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
```

**Trial 3**
```
PASS len=3 status=rejected tokens=0 msg='Please type a question.'
PASS len=4 status=rejected tokens=0 msg='Please type a question.'
PASS len=501 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
PASS len=800 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
PASS len=2000 status=rejected tokens=0 msg='That question is too long. Please keep it under 500 characters.'
```

## 4. Warm requests under 1.9s

**Trial 1**
```
cold (not counted) answered    6537 ms
warm               answered    6305 ms
warm               answered    7144 ms
warm               answered    7006 ms
warm               answered    2016 ms
warm               answered     851 ms
warm               answered    5551 ms
warm               answered    1160 ms
warm               answered    1115 ms
warm               answered     953 ms
warm               answered    5587 ms
```

**Trial 2**
```
cold (not counted) answered     849 ms
warm               answered     942 ms
warm               answered    2973 ms
warm               answered    1114 ms
warm               answered    4361 ms
warm               answered    1045 ms
warm               answered    1227 ms
warm               answered     802 ms
warm               answered     974 ms
warm               answered    1486 ms
warm               answered    3268 ms
```

**Trial 3**
```
cold (not counted) answered     869 ms
warm               answered     970 ms
warm               answered    2957 ms
warm               answered    1033 ms
warm               error      16318 ms
warm               answered    2434 ms
warm               answered   10808 ms
warm               answered     799 ms
warm               answered    2344 ms
warm               answered    1073 ms
warm               answered     919 ms
```

## 5. Original questions still contain expected phrase

**Trial 1**
```
FAIL expects='depth in one is worth more'
      Q: is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?
      A: No, depth in one club is worth more than breadth across five if you want a leadership position later. 

Source: thread_clubs.txt
PASS expects='16gb'
      Q: how many gb ram should my laptop be for cs course?
      A: Your laptop should have 16GB of RAM for CS courses. 

Source: thread_laptop_specs.txt
FAIL expects='48 hours'
      Q: how many hours does it take for a professor to answer email?
      A: Based on the provided documents, there is no information about how many hours it takes for a professor to answer an email. 

Source: thread_professor_email.txt
PASS expects='mediation'
      Q: how do i aproach my ra for room changes?
      A: You should talk to your RA early and frame the conversation as "we need help sorting this out" rather than asking to be moved. Skipping the mediation step slows down the process of getting a room change. 

Source: `thread_roommate_conflict.txt`
FAIL expects='science building'
      Q: apart from the library, is there a silent place one can study
      A: Based on the provided documents, the library third floor is the only place that reliably delivers silence, and the documents do not mention any silent places outside of the library. 

Source: thread_study_spots.txt
```

**Trial 2**
```
FAIL expects='depth in one is worth more'
      Q: is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?
      A: No, it is not advised. Depth in one club is worth more than breadth across five if you want a leadership position later (thread_clubs.txt).
PASS expects='16gb'
      Q: how many gb ram should my laptop be for cs course?
      A: Your laptop should have 16GB of RAM for CS courses (thread_laptop_specs.txt).
FAIL expects='48 hours'
      Q: how many hours does it take for a professor to answer email?
      A: Something went wrong while answering. Please try again.
PASS expects='mediation'
      Q: how do i aproach my ra for room changes?
      A: To approach your RA about a room change, talk to them early and frame the conversation as "we need help sorting this out" rather than asking to be moved. Skipping the mediation step will slow down the process. 

Source: thread_roommate_conflict.txt
FAIL expects='science building'
      Q: apart from the library, is there a silent place one can study
      A: Based on the provided document, the library third floor is noted as the only place that reliably delivers silence, and the text does not name any other silent study spots apart from the library (thread_study_spots.txt).
```

**Trial 3**
```
FAIL expects='depth in one is worth more'
      Q: is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?
      A: No, it is not advised. Depth in one club is worth more than breadth across five if you want a leadership position later (thread_clubs.txt).
PASS expects='16gb'
      Q: how many gb ram should my laptop be for cs course?
      A: Your laptop should have 16GB of RAM for CS courses. 

Source: thread_laptop_specs.txt
FAIL expects='48 hours'
      Q: how many hours does it take for a professor to answer email?
      A: I do not have enough information to answer how many hours it takes for a professor to answer email (thread_professor_email.txt).
FAIL expects='mediation'
      Q: how do i aproach my ra for room changes?
      A: According to `thread_roommate_conflict.txt`, you should talk to your RA early and frame the conversation as "we need help sorting this out" rather than asking to "move me."
FAIL expects='science building'
      Q: apart from the library, is there a silent place one can study
      A: Based on the provided document, the library's third floor is mentioned as the only place that reliably delivers silence, but the documents do not provide any silent study spots apart from the library (thread_study_spots.txt).
```
