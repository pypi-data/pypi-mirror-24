#HighlyProbable CLI

- Ability to connect with HighlyProbable Cloud AI Framework.
- Human understandable API made for developers to simplify getting AI tasks done
- Web Interface for this client is available on [HighlyProbable.com](highlyprobable.com)

## API Design

```python
>> hp = HighlyProbable(secret='<SECRET_KEY>')
>> hp.ai.help()

>> hp.ai.nlp.detect_language('<TEXT>')
>> hp.ai.geo.nearest_path_to('<MY_LONG>', '<MY_LAT>', '[<AVAILABLE_TARGETS>,]')
>> hp.ai.nlp.similarity.similars('<TARGET_TEXT>', '[<AVAILABLE_TEXTS>]')
>> hp.ai.nlp.similarity.is_similar('<TARGET_TEXT>', '<AVAILABLE_TEXT>')
>> dir(hp.ai)
nlp
geo
generic
...
```



