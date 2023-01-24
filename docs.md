# **Medical Records Generator** <!-- omit in toc -->

## **Contents** <!-- omit in toc -->
- [**About**](#about)
- [**Creating dictionary**](#creating-dictionary)
  - [**Setup**](#setup)
  - [**Default structure**](#default-structure)
    - [**Blocks**](#blocks)
    - [**Settings**](#settings)
    - [**Variables**](#variables)
  - [**Variants**](#variants)
    - [**Structure**](#structure)
      - [**Simple**](#simple)
      - [**Complex**](#complex)
  - [**Conditions**](#conditions)
    - [**Structure**](#structure-1)
    - [**Type**](#type)
      - [**EXISTENCE**](#existence)
      - [**VALUE**](#value)
      - [**AND**](#and)
      - [**OR**](#or)
      - [**NOT**](#not)
      - [**Combinations**](#combinations)
  - [**Scope**](#scope)
  - [**Examples**](#examples)
    - [**Date format examples**](#date-format-examples)
    - [**Time format examples**](#time-format-examples)
    - [**Variable examples**](#variable-examples)
    - [**Variants examples**](#variants-examples)
      - [**Simple variants**](#simple-variants)
      - [**Complex variants**](#complex-variants)
      - [**Combination of variants**](#combination-of-variants)
    - [**Conditions examples**](#conditions-examples)
      - [**EXISTENCE examples**](#existence-examples)
      - [**VALUE examples**](#value-examples)
      - [**AND examples**](#and-examples)
      - [**OR examples**](#or-examples)
      - [**NOT examples**](#not-examples)
      - [**Combinations examples**](#combinations-examples)


## **About**

The following document serves as a documentation of how to write a dictionary for the Medical Records Generator application.

## **Creating dictionary**

### **Setup**

**Format**\
The medical records generator works only with dictionaries written using the **json** format. 

**Name**\
The file name should correspond to the language code of the language the dictionary is written for. Language codes can be found at: https://www.fincher.org/Utilities/CountryLanguageList.shtml


### **Default structure**

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

#### **Blocks**

The whole generated report is divided into nine separate blocks. These blocks are: ```diagnosis, onset, admission, treatment, follow_up_imaging, post_acute_care, post_stroke_complications, etiology and discharge```. Every dictionary should contain all of the blocks even if left empty. \
Every block can contain multiple [variants](#variants) which specify the generated sentences.

#### **Settings**

**date_format**: A global setting that sets all the dates in the generated record based on the format. Leaving the setting empty will use the default date format. 
Default date format is ```%b %d %Y```.\
[Examples](#date-format-examples)

**time_format**: A global setting that sets all the times in the generated record based on the format. Leaving the setting empty will use the default time format. 
Default time format is ```"%H:%M"```.\
[Examples](#time-format-examples)

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

#### **Variables**

The "variables" part of the dictionary specifies custom translations for the given data. It is recommended not to delete any variable from the default structure as it may lead to unwanted logging errors. To ignore a variable, its translation should be left empty.\
[Examples](#variable-examples)

### **Variants**

As specified in the [blocks](#blocks) section, each block can contain multiple variants of generated senteces.

#### **Structure**

Each variant is written inside its own pair of curly brackets ```{}```.\
Those are all a part of the ```"variants": []``` bracket inside the given block.\
There are two types of structures for variants:
- [Simple](#simple)
- [Complex](#complex)

Variants can be combined.

##### **Simple**

The simple variant is composed of a ```condition``` and ```text```.\
If the ```condition``` is met, the corresponding ```text``` will be generated, otherwise it will be skipped.\
The simple structure looks as follows: 
```json
  {
    "condition": {},
    "text": "Text to generate if the condition is met."
  }
```
To see more specific uses, refer to [examples](#variants-examples).

```Text``` field can also use variables specified in the [scope](#scope) section. These variables are in the generation process replaced with their current values. For these variables to work properly, they have to be written inside ```${}```.\
Example:
```json
"text": "Onset on ${onset.onset_date} at ${onset.onset_time}. "
```
Here, the ```date_format``` and ```time_format``` settings will be used. With default settings the generated text might look like this: ```Onset on Oct 06 2022 at 00:36. ```
##### **Complex**

The complex variant is composed of a ```condition``` and a ```custom named block```.
If the ```condition``` is met, the corresponding ```custom named block``` will be executed, otherwise it will be skipped.\
A ```custom named block``` also contains the ```variants``` part. This makes it possible to nest multiple variants/custom named blocks. The name of the custom named block does not matter and is on the author of the dictionary to choose.\
The complex structure looks as follows:
```json
  {
    "condition": {},
    "blockForShowcase": {
      "variants": []
    }
  }
```
To see more specific uses, refer to [examples](#variants-examples).

### **Conditions**

Conditions are a part of every variant. They are used to decide which text to generate based on the context.

#### **Structure**

There are two kinds of structures of a condition. The structure is based on the ```type``` of a condition.
- First kind: 
  ```json
  {
    "condition": {
      "type": "",
      "scope": "",
      "value": ""
    }
  }
  ```
- Second kind:
  ```json
  {
    "condition": {
      "type": "",
      "conditions": []
    }
  }
  ```
To find out which kind to use refer to [types of conditions](#type).

#### **Type**

There are five types of conditions. These are:
- **EXISTENCE** (uses the **first** kind of structure of condition)
- **VALUE** (uses the **first** kind of structure of condition)
- **AND** (uses the **second** kind of structure of condition)
- **OR** (uses the **second** kind of structure of condition)
- **NOT** (uses the **second** kind of structure of condition)

##### **EXISTENCE**

```json
{
  "condition": {
    "type": "EXISTENCE",
    "scope": "scopeOfVariable",
    "value": true
  }
}
```
The **EXISTENCE** type of conditions checks wether the variable is existent or not. It contains ```scope``` and ```value``` fields.\
The ```scope``` defines the variable that the condition is about to check.\
The ```value``` can be either ```true``` or ```false```.
- Specifying the value to be ```true``` we are checking wether the variable specified in ```scope``` **does exist**.
- Specifying the value to be ```false``` we are checking wether the variable specified in ```scope``` **does not exist**.
  
[Examples](#existence-examples)

##### **VALUE**

```json
{
  "condition": {
    "type": "VALUE",
    "scope": "scopeOfVariable",
    "value": "test"
  }
}
```
The **VALUE** type of conditions checks wether the variable is equal to the ```value``` field. It contains ```scope``` and ```value``` fields.\
The ```scope``` defines the variable that the condition is about to check.\
The ```value``` field can be a number, text, boolean or any other type of value.\
[Examples](#value-examples)

##### **AND**

```json
{
  "condition": {
    "type": "AND",
    "conditions": []
  }
}
```
The **AND** condition check wether **all** of the conditions specified in the ```conditions``` field are satisfied. It contains only the ```conditions``` field. This condition allows nesting of other conditions.\
The ```conditions``` field is an array of conditions.\
[Examples](#and-examples)

##### **OR**

```json
{
  "condition": {
    "type": "OR",
    "conditions": []
  }
}
```
The **OR** condition check wether **atleast one** of the conditions specified in the ```conditions``` field is satisfied. It contains only the ```conditions``` field. This condition allows nesting of other conditions.\
The ```conditions``` field is an array of conditions.\
[Examples](#or-examples)

##### **NOT**

```json
{
  "condition": {
    "type": "NOT",
    "conditions": []
  }
}
```
The **NOT** condition negates and checks the conditions specified in the ```conditions``` field. It contains only the ```conditions``` field. This condition allows nesting of other conditions.\
The ```conditions``` field is an array of conditions.\
[Examples](#not-examples)

##### **Combinations**

All of the conditions above can be combined and nested into the conditions which support nesting.\
[Examples](#combinations-examples)

### **Scope**

Scope of the variables in this application is global. These variables are used in ```conditions``` and ```text```.

List of all scopes: 
| Variable                                | Possible values                                                                                                                                                              |
|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| diagnosis.stroke_type                   | ['ischemic', 'intracerebral hemorrhage', 'transient ischemic', 'subarachnoid hemorrhage', 'cerebral venous thrombosis', 'stroke mimics', 'undetermined']                     |
| diagnosis.aspects_score                 | int                                                                                                                                                                          |
| diagnosis.imaging_type                  | ['CT', 'CT CTA', 'CT CTA perfusion', 'MR DWI/FLAIR', 'MR DWI/FLAIR MRA', 'MR DWI/FLAIR MRA perfusion', 'done elsewhere', 'not done']                                         |
| diagnosis.occlusion_position            | string                                                                                                                                                                       |
| onset.onset_date                        | date                                                                                                                                                                         |
| onset.onset_time                        | time                                                                                                                                                                         |
| onset.wake_up_stroke                    | [True, False]                                                                                                                                                                |
| admission.admission_nihss               | integer                                                                                                                                                                      |
| admission.aspects_score                 | integer                                                                                                                                                                      |
| admission.admission_type                | ['ICU/stroke unit', 'monitored bed', 'standard bed']                                                                                                                         |
| treatment.thrombolysis_done             | [True, False]                                                                                                                                                                |
| treatment.thrombectomy_done             | [True, False]                                                                                                                                                                |
| treatment.thrombolysis_reasons          | ['done elsewhere', 'time window', 'mild deficit', 'consent', 'cost of treatment', 'transferred elsewhere', 'only MT', 'not available', 'other']                              |
| treatment.thrombectomy_reasons          | ['done elsewhere', 'time window', 'mild deficit', 'large vessel occlusion', 'disability', 'consent', 'cost of treatment', 'transferred elsewhere', 'not available', 'other'] |
| treatment.dtn                           | integer                                                                                                                                                                      |
| treatment.ivt_treatment                 | ['alteplase', 'tenecteplase', 'streptokinase', 'staphylokinase']                                                                                                             |
| treatment.ivt_dose                      | number                                                                                                                                                                       |
| treatment.dtg                           | integer                                                                                                                                                                      |
| treatment.tici_score                    | ['0', '1', '2A', '2B', '2C', '3', 'occlusion not confirmed']                                                                                                                 |
| treatment.dio                           | integer                                                                                                                                                                      |
| treatment.thrombectomy_transport        | [True, False]                                                                                                                                                                |
| treatment.tici_score_meaning            | Values from variables part of dictionary                                                                                                                                     |
| post_stroke_complications.complications | string                                                                                                                                                                       |
| discharge.discharge_date                | date                                                                                                                                                                         |
| discharge.discharge_destination         | ['home', 'same hospital', 'another hospital', 'social care', 'dead']                                                                                                         |
| discharge.nihss                         | integer                                                                                                                                                                      |
| discharge.mrs                           | integer                                                                                                                                                                      |
| discharge.contact_date                  | date                                                                                                                                                                         |
| discharge.mode_contact                  | ['telemedicine', 'visiting the clinic', 'mobile app', 'web app', 'no response', 'not contacted', Null]]                                                                      |
| discharge.discharge_medication          | string                                                                                                                                                                       |

### **Examples**

#### **Date format examples**
The following examples will work with this date ```"2023-01-17 18:48:49.503070"```

Default date format of the medical records generator is ```"%b %d %Y"```.

- Example 1: ```"date_format": ""```\
Formated date: Jan 17 2023\
Leaving the setting empty will use the default date format.

- Example 2: ```"date_format": "%a-%m-%y"```\
Formated date: Tue-01-23

- Example 3: ```"date_format": "%d. %B %Y"```\
Formated date: 17. January 2023

#### **Time format examples**

The following examples will work with this date ```"2023-01-17 18:48:49.503070"```

Default time format of the medical records generator is ```"%H:%M"```.

- Example 1: ```"time_format": ""```\
Formated time: 18:48\
Leaving the setting empty will use the default time format.

- Example 2: ```"time_format": "%I %p %S"```\
Formated time: 06 PM 49

- Example 3: ```"time_format": "Seconds: %S, Minutes: %M, Hour: %H"```\
Formated time: Seconds: 49, Minutes: 48, Hour: 18

#### **Variable examples**

- Example 1: 
  ```json
  {
    "therapies": {
    "physiotherapy": "physiotherapy",
    "ergotherapy": "ergo-therapy",
    "speechtherapy": ""
    }
  }
  ```
  This will make it so that if the patient was given physiotherapy, ergotherapy and speechtherapy, the generated report will translate the values as follows:
  - physiotherapy -> ```physiotherapy``` 
  - ergotherapy -> ```ergo-therapy```
  - speechtherapy -> ``` ```
  \
  The speechtherapy translation is left empty and therefore even if the data is pressent, no text will be generated.

- Example 2:
  ```json
  {
    "hospitalized_in": {
    "ICU/stroke unit": "ICU/stroke unit",
    "monitored bed": "monitored bed in hospital"  
    }
  }
  ```
  Notice that in this example, we are missing the field ```"standard bed": ""``` from the default structure. Although this will still generate the record properly, there will be logging error present about a missing variable. The generated report will translate the values as follows:
  - ICU/stroke unit -> ```ICU/stroke unit```
  - monitored bed -> ```monitored bed in hospital```
  - standard bed -> Logging error about a missing variable key

#### **Variants examples**

These examples are working with conditions, if you haven't already studied the [conditions](#conditions) section, these examples might be hard to understand.

##### **Simple variants**

- Example 1:
  ```json
  {
    "post_acute_care": {
      "variants": [
        {
          "condition": {
            "type": "VALUE",
            "scope": "post_acute_care.dysphagia_screening",
            "value": "no"
          },
          "text": "Patient screened for dysphagia but dysphagia not present. "
        },
        {
          "condition": {
            "type": "VALUE",
            "scope": "post_acute_care.dysphagia_screening",
            "value": "yes"
          },
          "text": "Patient diagnosed with dysphagia. "
        }
      ]
    }
  }
  ```
  In this example, there are two variants specified in the ```post_acute_care``` block. The first which checks for the value of ```dysphagia_screening``` to be equal to ```no```. If the condition would be met, the text would be generated.\
   After that the second variant is evaluated. Here the second variant checks for the value of ```dysphagia_screening``` to be equal to ```yes```. If this condition would be met, the text would be generated.\
  \
  As we can see though, these conditions contradict each other and thus, only one of the variant text would be generated.
  - If the value of ```dysphagia_screening``` is ```yes```.\
    Generated text is: ```Patient diagnosed with dysphagia. ```
  - If the value of ```dysphagia_screening``` is ```no```.\
    Generated text is: ```Patient screened for dysphagia but dysphagia not present. ```
  - If the value of ```dysphagia_screening``` is other than ```yes``` or ```no```.\
    No text is generated.

- Example 2:
  ```json
  {
    "admission": {
      "variants": [
        {
          "condition": {
            "type": "AND",
            "conditions": [
              {
                "type": "EXISTENCE",
                "scope": "admission.admission_nihss",
                "value": false
              },
              {
                "type": "EXISTENCE",
                "scope": "admission.aspects_score",
                "value": false
              }
            ]
          },
          "text": "NIHSS and ASPECT not performed. "
        },
        {
          "condition": {
            "type": "AND",
            "conditions": [
              {
                "type": "EXISTENCE",
                "scope": "admission.admission_nihss",
                "value": true
              },
              {
                "type": "EXISTENCE",
                "scope": "admission.admission_type",
                "value": false
              }
            ]
          },
          "text": "Baseline NIHSS ${admission.admission_nihss}. "
        }
      ]
    }
  }
  ```
  In this example, there are two variants specified in the ```admission``` block. Both variant conditions check the existence of ```admission_nihss``` and ```aspects_score``` at the same time. Notice that the conditions specify wether we check that the existence is true or the existence is false.
  - If both ```admission_nihss``` and ```aspects_score``` values are **not** existent.\
    Generated text is: ```NIHSS and ASPECT not performed. ```
  - If the ```admission_nihss``` value is existent and its value is ```3```, and ```aspects_score``` value is **not** existent.\
    Generated text is: ```Baseline NIHSS 3. ```. Here the ```${admission.admission_nihss}``` is replaced with the value.
  - Otherwise no text is generated.

##### **Complex variants**

- Example 1:
  ```json
  {
    "treatment": {
      "variants": [
        {
          "condition": {
            "type": "EXISTENCE",
            "scope": "treatment.thrombolysis_done",
            "value": true
          },
          "thrombolysis": {
            "variants": [
              {
                "condition": {
                  "type": "EXISTENCE",
                  "scope": "treatment.ivt_dose",
                  "value": true
                },
                "text": "First variant thrombolysis. "
              },
              {
                "condition": {
                  "type": "EXISTENCE",
                  "scope": "treatment.ivt_dose",
                  "value": false
                },
                "text": "Second variant thrombolysis. "
              }
            ]
          }
        },
        {
          "condition": {
            "type": "EXISTENCE",
            "scope": "treatment.thrombectomy_done",
            "value": true
          },
          "thrombectomy": {
            "variants": [
              {
                "condition": {
                  "type": "EXISTENCE",
                  "scope": "treatment.tici_score",
                  "value": true
                },
                "text": "First variant thrombectomy. "
              },
              {
                "condition": {
                  "type": "EXISTENCE",
                  "scope": "treatment.tici_score",
                  "value": false
                },
                "text": "Second variant thrombectomy. "
              }
            ]
          }
        }
      ]
    }
  }
  ```
  In this example, there are two variants specified in the ```treatment``` block. Each variant specifies its ```condition``` and a ```custom named block``` after that condition. If the condition is met, the following ```custom named block``` will be executed, otherwise its skipped. Those blocks being ```thrombolysis``` and ```thrombectomy```. Both of these blocks also specify two ```simple``` variants.
  - If ```thrombolysis_done``` is existent and ```ivt_dose``` is **not** existent, and also ```thrombectomy_done``` is existent and ```tici_score``` is existent.\
  Generated text is: ```Second variant thrombolysis. First variant thrombectomy. ```
  - If ```thrombolysis_done``` is existent and ```ivt_dose``` is existent, and also ```thrombectomy_done``` is **not** existent.\
  Generated text is: ```First variant thrombolysis. ```\
  Notice that the existence of ```ivt_dose``` in this case does not matter since the ```thrombectomy``` block will not be executed.
 
##### **Combination of variants**

- Example 1:
  ```json
  {
    "treatment": {
      "variants": [
        {
          "condition": {
            "type": "EXISTENCE",
            "scope": "treatment.thrombolysis_done",
            "value": true
          },
          "thrombolysis": {
            "variants": [
              {
                "condition": {
                  "type": "EXISTENCE",
                  "scope": "treatment.ivt_dose",
                  "value": true
                },
                "text": "First variant inside custom named block thrombolysis. "
              },
              {
                "condition": {
                  "type": "EXISTENCE",
                  "scope": "treatment.ivt_dose",
                  "value": false
                },
                "text": "Second variant inside custom named block thrombolysis. "
              }
            ]
          }
        },
        {
          "condition": {
            "type": "VALUE",
            "scope": "treatment.thrombolysis_reasons",
            "value": "time window"
          },
          "text": "Simple variant inside block treatment."
        }
      ]
    }
  }
  ```
  In this example, there are two variants specified in the ```treatment``` block. The first variant is a ```complex``` variant, while the second is a ```simple``` variant. The complex one specifies ```condition``` and ```custom named block```. The simple variant specifies ```condition``` and ```text```.

#### **Conditions examples**

##### **EXISTENCE examples**

- Example 1:
  ```json
  {
    "condition": {
      "type": "EXISTENCE",
      "scope": "scopeOfVariable",
      "value": true
    },
    "text": "Defined scope exists."
  }
  ```
  Our scope for this example is ```scopeOfVariable``` and the value is ```true```. Since the value is ```true``` we check wether our scope **exists**.
  - If ```scopeOfVariable``` is defined and has a non-empty value, the condition is met and we generate the specified ```text```.
  - If ```scopeOfVariable``` is not defined or has a empty value, the condition is not met and we skip the generation of ```text```.

- Example 2:
  ```json
  {
    "condition": {
      "type": "EXISTENCE",
      "scope": "scopeOfVariable",
      "value": false
    },
    "text": "Defined scope does not exist."
  }
  ```
  Our scope for this example is ```scopeOfVariable``` and the value is ```false```. Since the value is ```false``` we check wether our scope **does not exist**.
  - If ```scopeOfVariable``` is defined and has a non-empty value, the condition is not met and we skip the generation of ```text```.
  - If ```scopeOfVariable``` is not defined or has a empty value, the condition is met and we generate the specified ```text```.

- Example 3:
  ```json
  {
    "condition": {
      "type": "EXISTENCE",
      "scope": "scopeOfVariable",
      "value": true
    },
    "customNamedBlock": {
      "variants": []
    }
  }
  ```
  Our scope for this example is ```scopeOfVariable``` and the value is ```true```. Since the value is ```true``` we check wether our scope **exists**.
  - If ```scopeOfVariable``` is defined and has a non-empty value, the condition is met and we continue with executing the following ```customNamedBlock```.
  - If ```scopeOfVariable``` is not defined or has a empty value, the condition is not met and we skip the execution of the following ```customNamedBlock```.

##### **VALUE examples**

- Example 1:
  ```json
  {
    "condition": {
      "type": "VALUE",
      "scope": "stringExample",
      "value": "example"
    },
    "text": "Defined scope has the value 'example'."
  }
  ```
  Our scope for this example is ```stringExample``` and the value is ```example```. 
  - If ```stringExample``` matches the value specified, in our case ```example```, the condition is met and we generate specified ```text```.
  - If ```stringExample``` does not matche the value specified, in our case ```example```, the condition is not met and we skip the generation of ```text```.

- Example 2:
  ```json
  {
    "condition": {
      "type": "VALUE",
      "scope": "intExample",
      "value": 3
    },
    "text": "Defined scope has the value '3'."
  }
  ```
  Our scope for this example is ```intExample``` and the value is ```3```. 
  - If ```intExample``` matches the value specified, in our case ```3```, the condition is met and we generate specified ```text```.
  - If ```intExample``` does not matche the value specified, in our case ```3```, the condition is not met and we skip the generation of ```text```.

- Example 3:
  ```json
  {
    "condition": {
      "type": "VALUE",
      "scope": "stringExample",
      "value": "executeCustomNamedBlock"
    },
    "customNamedBlock": {
      "variants": []
    }
  }
  ```
  Our scope for this example is ```stringExample``` and the value is ```executeCustomNamedBlock```.
  - If ```stringExample``` matches the value specified, in our case ```executeCustomNamedBlock```, the condition is met and we continue with executing the following ```customNamedBlock```.
  - If ```stringExample``` does not match the value specified, in our case ```executeCustomNamedBlock```, the condition is not met and we skip the execution of the following ```customNamedBlock```.

##### **AND examples**

- Example 1:
  ```json
  {
    "condition": {
      "type": "AND",
      "conditions": [
        {
          "type": "EXISTENCE",
          "scope": "first",
          "value": true
        },
        {
          "type": "EXISTENCE",
          "scope": "second",
          "value": false
        }
      ]
    },
    "text": "Both conditions were satisfied. "
  }
  ```
  In this example there are two conditions that both **have** to be met to generate the specified ```text```.
  - If the first condition is met and the second condition is also met, we continue with generating the specified ```text```.
  - If any of the conditions is not met, we skip generating the specified ```text```.
  - Example: The scope ```first``` does exists therefore the first condition is met and the scope ```second``` does not exist, which means that the second condition is also met. (*Notice that we specified the value as ```false``` therefore we look for the scope to not exist.*). We generate the specified ```text```.

- Example 2:
  ```json
  {
    "condition": {
      "type": "AND",
      "conditions": [
        {
          "type": "EXISTENCE",
          "scope": "first",
          "value": true
        },
        {
          "type": "EXISTENCE",
          "scope": "second",
          "value": true
        },
        {
          "type": "VALUE",
          "scope": "third",
          "value": "Hello"
        }
      ]
    },
    "text": "All three conditions were satisfied. "
  }
  ```
  In this example there are three conditions and all three **have** to be met to generate the specified ```text```.
  - If all three conditions are met, we continue with generating the specified ```text```.
  - If any of the conditions is not met, we skip generating the specified ```text```.
  - Example: The scope ```first``` does exists therefore the first condition is met and the scope ```second``` does not exist, which means that the second condition is not met. Since one of the conditions were not met, we end the execution of our **AND** condition, and skip generating the text.

##### **OR examples**

- Example 1:
  ```json
  {
    "condition": {
      "type": "OR",
      "conditions": [
        {
          "type": "EXISTENCE",
          "scope": "first",
          "value": true
        },
        {
          "type": "EXISTENCE",
          "scope": "second",
          "value": false
        }
      ]
    },
    "text": "Atleast one condition was satisfied. "
  }
  ```
  In this example there are two conditions and **atleast one has** to be met to generate the specified ```text```.
  - If atleast one condition is met, we continue with generating the specified ```text```.
  - If none of the conditions is met, we skip generating the specified ```text```.
  - Example: The scope ```first``` does not exist, which means that the first condition is not met. Therefore we continue to the next condition. The scope ```second``` does not exist, which means that the second conditon is met. We generate the specified ```text```.
  
- Example 2:
  ```json
  {
    "condition": {
      "type": "OR",
      "conditions": [
        {
          "type": "EXISTENCE",
          "scope": "first",
          "value": true
        },
        {
          "type": "EXISTENCE",
          "scope": "second",
          "value": true
        },
        {
          "type": "VALUE",
          "scope": "third",
          "value": "Hello"
        }
      ]
    },
    "text": "Atleast one condition was satisfied. "
  }
  ```
  In this example there are three conditions and **atleast one has** to be met to generate the specified ```text```.
  - If atleast one condition is met, we continue with generating the specified ```text```.
  - If none of the conditions is met, we skip generating the specified ```text```.
  - Example: The scope ```first``` does exist, which means that the first condition is met. Since atleast one of the conditions were met, we end the execution of our **OR** condition, and we generate the specified ```text```.

##### **NOT examples**

- Example 1:
  ```json
  {
    "condition": {
      "type": "NOT",
      "conditions": [
        {
          "type": "VALUE",
          "scope": "example",
          "value": "other"
        }
      ]
    },
    "text": "The value of 'example' is not 'other'."
  }
  ```
  In this example we are negating one **VALUE** condition.
  - If the scope ```example``` matches the value ```other```, the inner condition is met which means that our **NOT** condition **is not** met. We skip the generation of specified ```text```.
  - If the scope ```example``` does not match the value ```other```, the inner condition is not met which means that our **NOT** condition **is** met. We generate the specified ```text```.

##### **Combinations examples**

- Example 1:
  ```json
  {
    "condition": {
      "type": "AND",
      "conditions": [
        {
          "type": "OR",
          "conditions": [
            {
              "type": "EXISTENCE",
              "scope": "FirstExistence",
              "value": true
            },
            {
              "type": "EXISTENCE",
              "scope": "SecondExistence",
              "value": true
            },
            {
              "type": "EXISTENCE",
              "scope": "ThirdExistence",
              "value": true
            }
          ]
        },
        {
          "type": "NOT",
          "conditions": [
            {
              "type": "VALUE",
              "scope": "ValueScope",
              "value": 7
            }
          ]
        }
      ]
    },
    "text": "The combined condition was met."
  }
  ```
  In this example we have a total of 7 conditions.
  - One **AND** condition
  - One **OR** condition
  - Three **EXISTENCE** conditions
  - One **NOT** condition
  - One **VALUE** condition
  
  For this example to generate the ```text``` our toplevel **AND** condition has to be met. Therefore the **OR** condition has to be met as well as the **NOT** condition.\
  For the **OR** condition to be met, atleast one of the **EXISTENCE** conditions has to be met.\
  For the **NOT** condition to be met, the **VALUE** condition must **not** be met.\
  - If ```FirstExistence``` or ```SecondExistence``` or ```ThirdExistence``` exist, and the value of ```ValueScope``` is **not** 7. We generate the specified ```text```.
  - Otherwise we skip the generation of specified ```text```.
