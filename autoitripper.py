import autoit_ripper

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT


class AutoItRipper(ServiceBase):
	def __init__(self, config=None):
		super(AutoItRipper, self).__init__(config)

	def start(self):
		self.log.debug("Autoit Ripper service started")

	def stop(self):
		self.log.debug("Autoit Ripper service ended")

	def execute(self, request):
		result = Result()
		file = request.file_path

		with open(file, "rb") as f:
			file_content = f.read()

		content_list = autoit_ripper.extract(data=file_content)

		if content_list:
			content = content_list[0][1].decode("utf-8")

			text_section = ResultSection('[DUMP RESULT]')
			text_section.add_line(content)
			text_section.set_heuristic(1)
			result.add_section(text_section)

			with open(self.working_directory + "script.au3", "w") as f:
				f.write(content)
			request.add_extracted(self.working_directory + 'script.au3', 'script.au3', 'This is the unpacked script')
		
		request.result = result