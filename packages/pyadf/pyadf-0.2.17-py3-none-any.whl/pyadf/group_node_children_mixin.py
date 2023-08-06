from pyadf.heading import Heading
from pyadf.paragraph import Paragraph

class GroupNodeChildrenMixin(object):

    def paragraph(self):
        p = Paragraph(self)
        self.content.append(p)
        return p

    def blockquote(self):
        # this sucks, but it avoids an error with a circular dependency
        # between BlockQuote and GroupNodeChildrenMixin
        from pyadf.block_quote import BlockQuote
        b = BlockQuote(self)
        self.content.append(b)
        return b

    def heading(self, level):
        h = Heading(level, parent=self)
        self.content.append(h)
        return h