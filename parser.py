import yaml
from gengine import Storyboard, Scene, Action


def build_actions(raw_actions):
    actions = []
    for k, ra in enumerate(raw_actions):
        try:
            actions.append(Action(ra["text"],
                                  ra["score"],
                                  ra["next_scene_name"]))
        except Exception as e:
            raise Exception("Invalid action (action={0})".format(str(ra))) from e
    return actions


def build_scenes(raw_scenes):
    scenes = {}
    for name, rs in raw_scenes.items():
        try:
            scenes[name] = Scene(name,
                                 rs["text"],
                                 build_actions(rs["actions"]) if rs.get("actions") is not None else None,
                                 rs.get("game_over"),
                                 rs.get("the_end"),
                                 rs.get("next_scene_name"))
        except Exception as e:
            raise Exception("Invalid scene (name={0} | scene={1})".format(name, str(rs))) from e
    return scenes


def parse_storyboard(path):
    content = None
    try:
        with open(path, "r") as stream:
            try:
                content = yaml.load(stream)
            except yaml.YAMLError as e:
                raise Exception("Failed to load the YAML file") from e
    except IOError as e:
        raise Exception("Failed to open the YAML file") from e

    try:
        title = content["title"]
        authors = content["authors"]
        target_audience = content["target_audience"]
        first_scene_name = content["first_scene_name"]
        scenes_raw = content["storyboard"]
        scenes = build_scenes(scenes_raw)
        return Storyboard(title, authors, target_audience, first_scene_name, scenes)
    except Exception as e:
        raise Exception("The provided file is an invalid format") from e
