How to call AppSheet API?

```
curl -X POST -i -H "Content-Type: application/json" -H "ApplicationAccessKey: V2-61wJZ-XOPjD-hG4Om-nIkfD-LESYh-1Iv8P-oy0hO-iQCR4" https://api.appsheet.com/api/v2/apps/763b2d4c-483f-4402-95e8-e6ca570acc2b/tables/bakeries/Action -d '{"Action":"Edit","Properties":{"Locale": "en-US"},"Rows":[{"bakeryname":"aloha","targetrevenue":9999}]}'
```

"Properties":{"Locale":"en-US","Location":"47.623098,-122.330184","Timezone":"PacificStandardTime"},