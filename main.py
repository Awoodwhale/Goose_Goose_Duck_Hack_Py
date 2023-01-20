import click
import webview
import logging
from backend.api import Api
import backend.utils.log as ulog


@click.command()
@click.option(
    "--gui",
    default=True,
    type=bool,
    help="Whether to open GUI window",
)
@click.option("--windows", type=int, default=1, help="Number of GUI windows")
@click.option(
    "--log",
    default=True,
    type=bool,
    help="Need to view log information",
)
@click.option(
    "--speed",
    type=float,
    help="Hack the player's current movement speed",
)
@click.option(
    "--wall",
    type=bool,
    help="Hack the player's cross the wall status",
)
@click.option(
    "--fog",
    type=bool,
    help="Hack the player's the fog of war",
)
@click.option(
    "--cd",
    type=bool,
    help="Hack the player's cooling state",
)
@click.option(
    "--showinfo",
    type=int,
    help="Display information of the target player",
)
def main(gui, windows, log, speed, wall, fog, cd, showinfo):
    if not log:
        ulog.Log.open_log = log
        logging.getLogger("pywebview").setLevel(logging.ERROR)
    api = Api()
    if gui:
        chinese = {
            "global.quitConfirmation": "确认退出吗?",
        }
        if windows < 1:
            click.echo("GUI窗口数量不能小于1")
            return
        for _ in range(windows):
            webview.create_window(
                title="Goose Goose Duck Hack",
                url="./frontend/index.html",
                width=900,
                height=750,
                resizable=True,
                text_select=False,
                confirm_close=True,
                js_api=api,
            )
        webview.start(localization=chinese, http_server=True, debug=False)
    else:
        if api.ready:
            api.update_players()
            if speed is not None:
                if speed < 0:
                    click.echo(f"修改速度不能小于0!")
                else:
                    res = api.hack_speed(float(speed))
                    click.echo(f"修改速度为{speed}{'成功!' if res else '失败! 请确保已进入房间!'}")
            if wall is not None:
                res = api.hack_wall(wall)
                click.echo(f"修改穿墙状态为{wall}{'成功!' if res else '失败! 请确保已进入房间!'}")
            if fog is not None:
                res = api.hack_fog(fog)
                click.echo(f"修改透视状态为{fog}{'成功!' if res else '失败! 请确保已进入房间!'}")
            if cd is not None:
                res = api.hack_cooldown(cd)
                click.echo(f"修改无CD状态为{cd}{'成功!' if res else '失败! 请确保已进入房间!'}")
            if showinfo is not None:
                if res := api.get_players_info():
                    click.echo(f"玩家[{showinfo}]的信息如下:\n{res[showinfo]}")
                else:
                    click.echo(f"读取玩家[{showinfo}]的信息失败! 请确保已进入游戏且该玩家存在!")
        else:
            click.echo("游戏进程未启动, 请在启动后使用!")
            return


if __name__ == "__main__":
    main()
