from medicalrecordgenerator.generator import generator
from medicalrecordgenerator.utils import load_utils

dictionary = load_utils.load_language("en_US")


def test_diagnosis():
    data = {"stroke_type": "ischemic",
            "imaging_type": "CT"}

    assert generator.generate_diagnosis(dictionary.diagnosis, dictionary.variables.occlusion_position, data) \
           == "Cerebral Infarction without occlusion CT angiogram. "

    data["occlusion_left_mca_m1"] = True

    assert generator.generate_diagnosis(dictionary.diagnosis, dictionary.variables.occlusion_position, data) \
           == "Cerebral Infarction due to occlusion of left MCA. "

    data["aspects_score"] = 8.0
    data["occlusion_right_mca_m1"] = True

    assert generator.generate_diagnosis(dictionary.diagnosis, dictionary.variables.occlusion_position, data) \
           == "Cerebral Infarction due to occlusion of left MCA, right MCA, ASPECT score 8.0. "


if __name__ == "__main__":
    print("Testing diagnosis")
    test_diagnosis()
    print("PASSED")

    print("Testing onset")
    test_diagnosis()
    print("PASSED")

    print("Everything passed")
