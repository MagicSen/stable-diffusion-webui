from modules import scripts, scripts_postprocessing, shared

# 继承自Script类
class ScriptPostprocessingForMainUI(scripts.Script):
    def __init__(self, script_postproc):
        # 变量: 注释的类型 = 值， 等效于 变量 = 值
        self.script: scripts_postprocessing.ScriptPostprocessing = script_postproc
        self.postprocessing_controls = None

    def title(self):
        return self.script.name

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        self.postprocessing_controls = self.script.ui()
        return self.postprocessing_controls.values()

    def postprocess_image(self, p, script_pp, *args):
        args_dict = {k: v for k, v in zip(self.postprocessing_controls, args)}

        pp = scripts_postprocessing.PostprocessedImage(script_pp.image)
        pp.info = {}
        # 执行脚本，接受图像以及后处理参数
        self.script.process(pp, **args_dict)
        # 收集脚本处理结果
        p.extra_generation_params.update(pp.info)
        # 更新图像
        script_pp.image = pp.image


def create_auto_preprocessing_script_data():
    from modules import scripts
    # 加载生效的后处理脚本
    res = []

    for name in shared.opts.postprocessing_enable_in_main_ui:
        script = next(iter([x for x in scripts.postprocessing_scripts_data if x.script_class.name == name]), None)
        if script is None:
            continue

        constructor = lambda s=script: ScriptPostprocessingForMainUI(s.script_class())
        res.append(scripts.ScriptClassData(script_class=constructor, path=script.path, basedir=script.basedir, module=script.module))

    return res
