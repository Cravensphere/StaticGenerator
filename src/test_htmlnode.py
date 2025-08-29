def test_eq(self):
    html1 = HTMLNode("div", "Hello", [], {"class": "container"})
    html2 = HTMLNode("div", "Hello", [], {"class": "container"}) 

    if html1.tag == html2.tag and html1.value == html2.value and html1.children == html2.children and html1.props == html2.props:
        return True
    return False

def test_neq(self):
    html1 = HTMLNode("div", "Hello", [], {"class": "container"})
    html2 = HTMLNode("p", "Hello", [], {"class": "container"}) 

    if html1.tag == html2.tag and html1.value == html2.value and html1.children == html2.children and html1.props == html2.props:
        return False
    return True

def test_repr(self):
    html = HTMLNode("div", "Hello", [], {"class": "container"})
    return repr(html) == "HTMLNode(div, Hello, [], {'class': 'container'})"

def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)