# Medical Records Generator <!-- omit in toc -->

## Contents <!-- omit in toc -->
- [About](#about)
- [Creating dictionary](#creating-dictionary)
  - [Setup](#setup)
  - [Default structure](#default-structure)
    - [Settings](#settings)
    - [Variables](#variables)
  - [Conditions](#conditions)
  - [Examples](#examples)
    - [Date format example](#date-format-example)
    - [Time format example](#time-format-example)


## About

TBD

## Creating dictionary

### Setup

**Format**
The medical records generator works only with dictionaries written using **json**

**Name**
The file name should correspond to the language code of the language the dictionary is written for. Language codes can be found at: https://www.fincher.org/Utilities/CountryLanguageList.shtml


### Default structure

The following is the default structure that every dictionary, that is to be used by this application, should follow. *Disclaimer: For the generator to work correctly do not remove any of the parts of the following json file.*
```json
{
  "diagnosis": {
    "variants": []
  },
  "onset": {
    "variants": []
  },
  "admission": {
    "variants": []
  },
  "treatment": {
    "variants": []    
  },
  "follow_up_imaging": {
    "variants": [] 
  },
  "post_acute_care": {
    "variants": [] 
  },
  "post_stroke_complications": {
    "variants": [] 
  },
  "etiology": {
    "variants": [] 
  },
  "discharge": {
    "variants": [] 
  },
  "settings": {
    "date_format": "",
    "time_format": ""
  },
  "variables": {
    "imaging_type": {
      "CT": "",
      "CT CTA": "",
      "CT CTA perfusion": "",
      "MR DWI/FLAIR": "",
      "MR DWI/FLAIR MRA": "",
      "MR DWI/FLAIR MRA perfusion": "",
      "done elsewhere": "",
      "not done": ""
    },
    "occlusion_position": {
      "occlusion_left_mca_m1": "",
      "occlusion_left_mca_m2": "",
      "occlusion_left_mca_m3": "",
      "occlusion_left_aca": "",
      "occlusion_left_pca_p1": "",
      "occlusion_left_pca_p2": "",
      "occlusion_left_cae": "",
      "occlusion_left_cai": "",
      "occlusion_right_mca_m1": "",
      "occlusion_right_mca_m2": "",
      "occlusion_right_mca_m3": "",
      "occlusion_right_aca": "",
      "occlusion_right_pca_p1": "",
      "occlusion_right_pca_p2": "",
      "occlusion_right_cae": "",
      "occlusion_right_cai": "",
      "occlusion_ba": "",
      "occlusion_va": ""
    },
    "hospitalized_in": {
      "ICU/stroke unit": "",
      "monitored bed": "",
      "standard bed": ""
    },
    "ivt_treatment": {
      "alteplase": "",
      "tenecteplase": "",
      "streptokinase": "",
      "staphylokinase": ""
    },
    "no_thrombolysis_reason": {
      "done elsewhere": "",
      "time window": "",
      "mild deficit": "",
      "consent": "",
      "cost of treatment": "",
      "transferred elsewhere": "",
      "only MT": "",
      "not available": "",
      "other": ""
    },
    "no_thrombectomy_reason": {
      "done elsewhere": "",
      "time window": "",
      "mild deficit": "",
      "large vessel occlusion": "",
      "disability": "",
      "consent": "",
      "cost of treatment": "",
      "transferred elsewhere": "",
      "not available": "",
      "other": ""
    },
    "post_treatment_findings": {
      "post_treatment_infarction": "",
      "post_treatment_no_bleeding": "",
      "post_treatment_remote": "",
      "post_treatment_hi_i": "",
      "post_treatment_hi_ii": "",
      "post_treatment_ph_i": "",
      "post_treatment_ph_ii": ""
    },
    "post_stroke_complications": {
      "post_stroke_pneumonia": "",
      "post_stroke_dvt": "",
      "post_stroke_embolism": "",
      "post_stroke_infection": "",
      "post_stroke_sores": "",
      "post_stroke_sepsis": "",
      "post_stroke_extension": "",
      "post_stroke_other": "",
      "post_stroke_none": ""
    },
    "therapies": {
      "physiotherapy": "",
      "ergotherapy": "",
      "speechtherapy": ""
    },
    "etiology": {
      "etiology_large_artery": "",
      "etiology_cardioembolism": "",
      "etiology_other": "",
      "etiology_cryptogenic_stroke": "",
      "etiology_small_vessel": ""
    },
    "discharge_destination": {
      "home": "",
      "same hospital": "",
      "another hospital": "",
      "social care": "",
      "dead": ""
    },
    "medications": {
      "discharge_antidiabetics": "",
      "discharge_antihypertensives": "",
      "discharge_asa": "",
      "discharge_cilostazol": "",
      "discharge_clopidrogel": "",
      "discharge_ticagrelor": "",
      "discharge_ticlopidine": "",
      "discharge_prasugrel": "",
      "discharge_dipyridamol": "",
      "discharge_warfarin": "",
      "discharge_dabigatran": "",
      "discharge_rivaroxaban": "",
      "discharge_apixaban": "",
      "discharge_edoxaban": "",
      "discharge_statin": "",
      "discharge_heparin": "",
      "discharge_other": "",
      "discharge_anticoagulant_recommended": "",
      "discharge_other_antiplatelet": "",
      "discharge_other_anticoagulant": "",
      "discharge_any_anticoagulant": "",
      "discharge_any_antiplatelet": ""
    },
    "tici_score_meaning": {
      "tici_score_0": "",
      "tici_score_1": "",
      "tici_score_2A": "",
      "tici_score_2B": "",
      "tici_score_2C": "",
      "tici_score_3": ""
    }
  }
}
```
#### Settings

**date_format**: A global setting that sets all the dates in the generated record based on the format. Leaving the setting empty will use the default date format. 
Default date format is ```%b %d %Y```.
[Examples](#date-format-example)

**time_format**: A global setting that sets all the times in the generated record based on the format. Leaving the setting empty will use the default time format. 
Default time format is ```"%H:%M"```.
[Examples](#time-format-example)

Format is specified using a combination of directives. The available directives can be seen in the table below. To see examples of the formats follow the [link](#examples).

| Directive | Meaning                                                                                                                                          | Output Format        |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| %a        | Abbreviated weekday name.                                                                                                                        | Sun, Mon, …          |
| %A        | Full weekday name.                                                                                                                               | Sunday, Monday, …    |
| %w        | Weekday as a decimal number.                                                                                                                     | 0, 1, …, 6           |
| %d        | Day of the month as a zero added decimal.                                                                                                        | 01, 02, …, 31        |
| %#d       | Day of the month as a decimal number.                                                                                                            | 1, 2, …, 30          |
| %b        | Abbreviated month name.                                                                                                                          | Jan, Feb, …, Dec     |
| %B        | Full month name.                                                                                                                                 | January, February, … |
| %m        | Month as a zero added decimal number.                                                                                                            | 01, 02, …, 12        |
| %#m       | Month as a decimal number.                                                                                                                       | 1, 2, …, 12          |
| %y        | Year without century as a zero added decimal number.                                                                                             | 00, 01, …, 99        |
| %#y       | Year without century as a decimal number.                                                                                                        | 0, 1, …, 99          |
| %Y        | Year with century as a decimal number.                                                                                                           | 2013, 2019 etc.      |
| %H        | Hour (24-hour clock) as a zero added decimal number.                                                                                             | 00, 01, …, 23        |
| %#H       | Hour (24-hour clock) as a decimal number.                                                                                                        | 0, 1, …, 23          |
| %I        | Hour (12-hour clock) as a zero added decimal number.                                                                                             | 01, 02, …, 12        |
| %#I       | Hour (12-hour clock) as a decimal number.                                                                                                        | 1, 2, … 12           |
| %p        | Locale’s AM or PM.                                                                                                                               | AM, PM               |
| %M        | Minute as a zero added decimal number.                                                                                                           | 00, 01, …, 59        |
| %#M       | Minute as a decimal number.                                                                                                                      | 0, 1, …, 59          |
| %S        | Second as a zero added decimal number.                                                                                                           | 00, 01, …, 59        |
| %#S       | Second as a decimal number.                                                                                                                      | 0, 1, …, 59          |
| %f        | Microsecond as a decimal number, zero added on the left.                                                                                         | 000000 – 999999      |
| %z        | UTC offset in the form +HHMM or -HHMM.                                                                                                           |                      |
| %Z        | Time zone name.                                                                                                                                  |                      |
| %j        | Day of the year as a zero added decimal number.                                                                                                  | 001, 002, …, 366     |
| %#j       | Day of the year as a decimal number.                                                                                                             | 1, 2, …, 366         |
| %U        | Week number of the year (Sunday as the first day of the week). All days in a new year preceding the first Sunday are considered to be in week 0. | 00, 01, …, 53        |
| %W        | Week number of the year (Monday as the first day of the week). All days in a new year preceding the first Monday are considered to be in week 0. | 00, 01, …, 53        |

#### Variables


### Conditions

### Examples

#### Date format example
The following examples will work with this date ```"2023-01-17 18:48:49.503070"```

Default date format of the medical records generator is ```"%b %d %Y"```.

- Example 1: ```"date_format": ""```
Leaving the setting empty will use the default date format.
Formated date: Jan 17 2023
- Example 2: ```"date_format": "%a-%m-%y"```
Formated date: Tue-01-23
- Example 3: ```"date_format": "%d. %B %Y"```
Formated date: 17. January 2023

#### Time format example

The following examples will work with this date ```"2023-01-17 18:48:49.503070"```

Default time format of the medical records generator is ```"%H:%M"```.

- Example 1: ```"time_format": ""```
Leaving the setting empty will use the default time format.
Formated time: 18:48
- Example 2: ```"time_format": "%I %p %S"```
Formated time: 06 PM 49
- Example 3: ```"time_format": "Seconds: %S, Minutes: %M, Hour: %H"```
Formated time: Seconds: 49, Minutes: 48, Hour: 18