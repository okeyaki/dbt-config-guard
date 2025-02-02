<!--
Generated from `etc/jinja2/templates/_rule.md.j2`
-->

# model_columns.data_tests.required

## Description

Model columns should have the specified data tests.

## Schema

<pre><code>{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "additionalProperties": false,
  "description": "Model columns should have the specified data tests.",
  "properties": {
    "data_test_names": {
      "description": "Required data test names.",
      "items": {
        "examples": [
          "not_null"
        ],
        "type": "string"
      },
      "type": "array"
    }
  },
  "title": "model_columns.data_tests.required",
  "type": "object"
}</code></pre>
