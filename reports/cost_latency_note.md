# SCOOBYDO AI – Cost and Latency Note

## API usage

The input dataset contains 25 registration rows. The corrected program identifies eight exact repeated source entries before making a Gemini request. The remaining 17 distinct entries require extraction requests in a successful full run (including R25, which is not text-identical to R16 and is detected as a duplicate after cleaning).

## Request spacing and latency

The corrected program enforces a minimum interval of 5.2 seconds between Gemini requests. For 17 requests, the intentional spacing between request starts is approximately 83.2 seconds across 16 intervals; total runtime is longer because Gemini response time and any retries add time. Actual average response latency was not separately measured.

## API cost

The project was tested using the Gemini API free tier. No paid usage is assumed in this estimate. Actual availability, quotas and pricing depend on the selected model and the account's current terms. A free-tier request limit can still cause HTTP 429 errors.

## Error handling

The corrected application retries selected temporary errors, including rate-limit and service-unavailable responses, using retry delays and request spacing. Retries reduce the impact of temporary failures but cannot bypass an exhausted quota or guarantee service availability.

## Conclusion

Python cleaning, validation, duplicate checks and report generation run locally. Gemini is used for extracting structured fields from distinct registration messages. API usage and actual processing time should be measured again if the dataset or model changes.
