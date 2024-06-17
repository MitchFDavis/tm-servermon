from pyplanet.apps.config import AppConfig
from pyplanet.core.events import Callback, Signal
from pyplanet.core.exceptions import SignalGlueStop
from pyplanet.core.instance import Controller
import logging
import nats

logger = logging.getLogger(__name__)


class GamestatsApp(AppConfig):
	game_dependencies = ['trackmania_next',]
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	async def on_init(self):
		self.instance.nc = await nats.connect("nats://localhost:4222")
		await super().on_init()

	async def on_start(self):
		await self.instance.nc.publish("meta", b'app started')
		await super().on_start()

	async def on_stop(self):
		await self.instance.nc.publish("meta", b'app stopped')
		await super().on_stop()

	async def on_destroy(self):
		await self.instance.nc.drain()
		await super().on_destroy()

async def handle_testevent(source, signal, **kwargs):
	logging.info(source)
	await Controller.instance.nc.publish(signal.raw_signal.code, str(source).encode())


async def handle_waypoint(source, signal, **kwargs):
	logging.info(source)
	#player = await Controller.instance.player_manager.get_player(login=source['login'])
	await Controller.instance.nc.publish(signal.raw_signal.code, str(source).encode())

async def handle_chat(source, signal, **kwargs):
	player_uid, player_login, text, cmd = source
	try:
		player = await Controller.instance.player_manager.get_player(login=player_login, lock=True)
	except:
		raise SignalGlueStop()
	return dict(
		# Set cmd to False to prevent PyPlanet from processing commands
		player=player, text=text, cmd=False
	)

waypoint = Callback(
	call='Script.Trackmania.Event.WayPoint',
	namespace='trackmania',
	code='waypoint',
	target=handle_waypoint,
)

player_chat = Callback(
	call='ManiaPlanet.PlayerChat',
	namespace='maniaplanet',
	code='player_chat',
	target=handle_chat,
)

socres = Callback(
	call='Script.Trackmania.Scores',
	namespace='trackmania',
	code='scores',
	target=handle_testevent,
)
