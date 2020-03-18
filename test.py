import unittest
import filecmp
import generate
import glob, os

RST_PATH = "test/source/"
OUTPUT_PATH = "./output/"
EXPECTED_PATH = "test/expected_output/"


class Test(unittest.TestCase):
    def test_list(self):
        rst_path = "test/source/"
        files = ['test/source\\contact.rst', 'test/source\\index.rst']
        rst_file = [file for file in glob.glob(os.path.join(rst_path, '*.rst'))]
        self.assertTrue(sorted(files) == sorted(rst_file))

    def test_read(self):
        rst_path = "test/source/"
        contact = generate.read_file(os.path.join(rst_path, "contact.rst"))
        index = generate.read_file(os.path.join(rst_path, "contact.rst"))

        contact_expected = ({'title': 'Contact us!', 'layout': 'base.html'},
                            'Write an email to contact@example.com.')
        index_expected = ({'title': 'My awesome site', 'layout': 'home.html'}, 'blah blah')
        self.assertTrue(contact, contact_expected)
        self.assertTrue(index, index_expected)

    def test_write(self):
        OUTPUT_PATH = "./create_output/"
        generate.write_output("test_write", "Works", OUTPUT_PATH)
        output_folder = "create_output"
        created = False
        works = False
        for file in os.listdir('./'):
            print(file)
            if file == output_folder:
                created = True

        if (created):
            f = open(os.path.join(OUTPUT_PATH, "test_write.html"))
            text = f.read()
            if (text == "Works"):
                works = True

        self.assertTrue(created, True)
        self.assertTrue(works, True)

    def test_output(self):
        generate.generate_site(RST_PATH, OUTPUT_PATH)
        self.assertTrue(filecmp.cmp(EXPECTED_PATH + str("contact.html"), OUTPUT_PATH + str("contact.html")));
        self.assertTrue(filecmp.cmp(EXPECTED_PATH + str("index.html"), OUTPUT_PATH + str("index.html")));
