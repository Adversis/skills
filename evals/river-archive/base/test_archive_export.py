import unittest

from archive_export import render_export, request_export


class ExportPolicy(unittest.TestCase):
    def test_permitted_export(self):
        jobs = []
        self.assertTrue(request_export("east", "east", jobs))
        self.assertEqual(render_export(jobs.pop()), {"tenant": "east"})

    def test_denied_export(self):
        jobs = []
        request_export("east", "west", jobs)
        self.assertEqual(jobs, [], "A denied export must leave the queue empty")
