from core.renderer import TableRenderer


class TestTableRenderer:
    def test_render_does_not_crash(self, sample_report_data):
        """Просто проверяем, что рендеринг не вызывает ошибок."""
        renderer = TableRenderer(sample_report_data)
        renderer.render()

    def test_render_empty_data(self):
        """Тест рендеринга пустого отчета."""
        renderer = TableRenderer({})
        renderer.render()
