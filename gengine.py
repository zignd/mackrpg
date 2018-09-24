class Action:
    def __init__(self, text, score, next_scene_name):
        self.text = text
        self.score = score
        self.next_scene_name = next_scene_name


class Scene:
    def __init__(self, name, text, actions=None, game_over=False, the_end=False, next_scene_name=None):
        self.name = name
        self.text = text
        self.actions = actions
        self.game_over = game_over
        self.the_end = the_end
        self.next_scene_name = next_scene_name

        self.selected_action = None

    def act(self):
        print("\n{0}\n".format(self.text))

        if self.actions is not None:
            action = None
            ok = False
            while not ok:
                for index, action in enumerate(self.actions):
                    print("{0}) {1}".format(index + 1, action.text))
                print("")
                try:
                    selected_action_index = int(input("> ")) - 1

                    if 0 <= selected_action_index < len(self.actions):
                        action = self.actions[selected_action_index]
                        ok = True
                        continue
                except ValueError:
                    pass
                print("Ação inválida, tente novamente")
            self.selected_action = action
        else:
            input("> [Enter]")

        if self.game_over or self.the_end:
            return

    def get_max_score(self):
        max_score = 0
        if self.actions is None:
            return max_score
        for index, action in enumerate(self.actions):
            if action.score > max_score:
                max_score = action.score
        return max_score


class Storyboard:
    def __init__(self, title, authors, target_audience, first_scene_name, scenes):
        self.title = title
        self.authors = authors
        self.target_audience = target_audience
        self.first_scene_name = first_scene_name
        self.scenes = scenes
        self.current_score = 0
        self.last_scene = None

    def displayHeader(self):
        print("Título: {0}".format(self.title))
        print("Autores:")
        for index, author in enumerate(self.authors):
            print(" - {0}".format(author))
        print("Público alvo: {0}".format(self.target_audience))
        print("Manual: As interações com o jogo consistem em escolher ações através de números e confirmações com o " +
              "botão Enter. O caractere '>' indica uma soliticação de interação através de números, mas quando " +
              "estiver acompanhado de um '[Enter]' você deverá aperta Enter apenas.")

    def play(self):
        self.current_score = 0
        self.last_scene = self._play(self.scenes.get(self.first_scene_name))

        if self.last_scene.game_over:
            print("\nFALHOU EM COMPLETAR O JOGO D:\n")
        else:
            print("\nJOGO COMPLETO :D\n")

    def _play(self, scene):
        scene.act()

        if scene.selected_action is not None:
            action = scene.selected_action
            self.current_score += action.score
            return self._play(self.scenes.get(action.next_scene_name))
        elif scene.next_scene_name is not None:
            return self._play(self.scenes.get(scene.next_scene_name))
        else:
            return scene

    def report_score(self):
        max_score = 0
        for key, scene in self.scenes.items():
            max_score += scene.get_max_score()
        score_ratio = (self.current_score/max_score)*100
        ranking = Storyboard.rank(score_ratio)

        print("Relatório de pontuação\n",
              "Pontuação máxima possível: {0}\n".format(max_score),
              "Sua pontuação: {0}\n".format(self.current_score),
              "Taxa de acerto: {0:.2f}%\n".format(score_ratio),
              "Classificação: {0}\n".format(ranking))

    @staticmethod
    def rank(score_ratio):
        if 0 <= score_ratio <= 10:
            return "Noob"
        elif 10 < score_ratio <= 20:
            return "Novato"
        elif 20 < score_ratio <= 40:
            return "Iniciante"
        elif 40 < score_ratio <= 60:
            return "Regular"
        elif 60 < score_ratio <= 70:
            return "Sobrevivente"
        elif 70 < score_ratio <= 85:
            return "Sobrevivente Experiente"
        else:
            return "Gênio da Sobrevivência"
