import pytest
from scripts.player_data import extract_player_data, career_data


# testing extracting female JS data
def test_extract_female():
    with open("tests/test_data/female_career.js", "r") as f:
        text = f.read()

    player_df = extract_player_data(text)

    assert len(player_df) == 3
    assert "obday" in player_df.columns
    assert player_df["opp"].iloc[0] == "Anne Miller"
    assert player_df["obday"].iloc[0] == "19770119"


# testing extracting male JS data
def test_extract_male():
    with open("tests/test_data/male_career.js", "r") as f:
        text = f.read()

    player_df = extract_player_data(text)

    assert len(player_df) == 3
    assert "obday" in player_df.columns
    assert player_df["opp"].iloc[0] == "Guillermo Platel"
    assert player_df["obday"].iloc[0] == "22.264202601"


# testing processing female data
def test_career_female():
    with open("tests/test_data/female_career.js", "r") as f:
        text = f.read()

    player_df = extract_player_data(text)
    result = career_data(text, "1981-09-26")

    assert len(result) == 3
    assert "age_difference" in result.columns
    assert result["opp_age"].notna().all()
    assert result["age_difference"].notna().all()


# testing processing male data
def test_career_male():
    with open("tests/test_data/male_career.js", "r") as f:
        text = f.read()

    player_df = extract_player_data(text)
    result = career_data(text, "1986-06-03")

    assert len(result) == 3
    assert "age_difference" in result.columns
    assert result["opp_age"].iloc[0] == pytest.approx(22.264202601)
    assert result["age_difference"].notna().all()