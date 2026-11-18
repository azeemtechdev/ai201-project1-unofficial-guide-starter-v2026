# Capstone run: after  (2026-11-17 22:16)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Real timeout gives clear message + error/timeout log row | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every request logged (10 new lines, 1 forced failure) | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 3. Invalid input rejected, 0 tokens, logged | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Warm requests under 1.9s | 9 of 10 | 8/10 | 7/10 | 4/10 | MISSED |
| 5. Original questions still contain expected phrase | 5 of 5 | 2/5 | 2/5 | 3/5 | MISSED |

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
cold (not counted) answered    2592 ms
warm               answered     983 ms
warm               answered    1956 ms
warm               answered    1034 ms
warm               answered    1534 ms
warm               answered    2058 ms
warm               answered    1074 ms
warm               answered     950 ms
warm               answered    1645 ms
warm               answered    1278 ms
warm               answered     916 ms
```

**Trial 2**
```
cold (not counted) answered    1305 ms
warm               answered    1147 ms
warm               answered     904 ms
warm               answered     909 ms
warm               answered    1016 ms
warm               answered    1310 ms
warm               answered    1124 ms
warm               error      21482 ms
warm               answered   12923 ms
warm               answered    4712 ms
warm               answered    1734 ms
```

**Trial 3**
```
cold (not counted) answered    1116 ms
warm               answered    2694 ms
warm               answered    1559 ms
warm               answered    1460 ms
warm               answered    1811 ms
warm               answered    2228 ms
warm               answered    1219 ms
warm               answered    2047 ms
warm               answered    2340 ms
warm               answered    2520 ms
warm               answered    2967 ms
```

## 5. Original questions still contain expected phrase

**Trial 1**
```
FAIL expects='depth in one is worth more'
      Q: is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?
      A: No, depth in one club is considered worth more than breadth across five if you want a leadership position later (*thread_clubs.txt*).
PASS expects='16gb'
      Q: how many gb ram should my laptop be for cs course?
      A: Based on the documents, your laptop should have 16GB of RAM for CS courses (thread_laptop_specs.txt).
PASS expects='48 hours'
      Q: how many hours does it take for a professor to answer email?
      A: Based on the provided documents, the response time for a professor varies enormously. If the syllabus does not state a response window, you should assume 48 hours. 

Source: thread_professor_email.txt
FAIL expects='mediation'
      Q: how do i aproach my ra for room changes?
      A: Something went wrong while answering. Please try again.
FAIL expects='science building'
      Q: apart from the library, is there a silent place one can study
      A: Based on the provided documents, the text does not mention any silent study places outside of the library. 

Source: `thread_study_spots.txt`
```

**Trial 2**
```
FAIL expects='depth in one is worth more'
      Q: is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?
      A: No, it is not advised. Depth in one club is worth more than breadth across five if you want a leadership position later. 

(Source: thread_clubs.txt)
PASS expects='16gb'
      Q: how many gb ram should my laptop be for cs course?
      A: Your laptop should have 16GB of RAM for CS courses (thread_laptop_specs.txt).
FAIL expects='48 hours'
      Q: how many hours does it take for a professor to answer email?
      A: According to the general rule found, you should assume a 48-hour response window if the syllabus does not state one. (Source: thread_professor_email.txt)
PASS expects='mediation'
      Q: how do i aproach my ra for room changes?
      A: To approach your RA for a room change, talk to them early and frame the conversation as "we need help sorting this out" rather than asking to move. Room changes are possible, but the process starts with mediation because skipping that step slows it down. 

Source: thread_roommate_conflict.txt
FAIL expects='science building'
      Q: apart from the library, is there a silent place one can study
      A: Based on the provided documents, the text does not mention any silent places to study apart from the library. 

Source: thread_study_spots.txt
```

**Trial 3**
```
FAIL expects='depth in one is worth more'
      Q: is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?
      A: No, it is not advised. If you want a leadership position later, depth in one club is worth more than breadth across five. 

Source: thread_clubs.txt
PASS expects='16gb'
      Q: how many gb ram should my laptop be for cs course?
      A: Your laptop should have 16GB of RAM for CS courses (thread_laptop_specs.txt).
PASS expects='48 hours'
      Q: how many hours does it take for a professor to answer email?
      A: If the syllabus states a response window, that is honoured; otherwise, you should assume 48 hours. 

Source: thread_professor_email.txt
PASS expects='mediation'
      Q: how do i aproach my ra for room changes?
      A: To approach your RA for a room change, talk to them early and frame the conversation as "we need help sorting this out" rather than asking to move. Room changes require mediation first, and skipping that step will only slow the process down. 

Source: `thread_roommate_conflict.txt`
FAIL expects='science building'
      Q: apart from the library, is there a silent place one can study
      A: Based on the provided documents, there is no mention of a silent study place outside of the library. (Source: thread_study_spots.txt)
```
