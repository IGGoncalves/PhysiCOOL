"""Script to test the pcxml module of the PhysiCOOL package."""
import unittest
from shutil import copyfile
from xml.etree import ElementTree

from physicool import pcxml
from configdata import *


class ReadDataTest(unittest.TestCase):
    def setUp(self):
        """Reads the data into an ElementTree to be accessed by the class methods."""
        self.tree = ElementTree.parse(CONFIG_PATH)

    def test_parse_domain(self):
        """Asserts that the <domain> data is correctly read."""
        data = pcxml.parse_domain(tree=self.tree, path="domain")
        self.assertEqual(EXPECTED_DOMAIN_READ, data)

    def test_parse_domain_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_domain, self.tree, "overall")

    def test_parse_overall(self):
        """Asserts that the <overall> data is correctly read."""
        data = pcxml.parse_overall(tree=self.tree, path="overall")
        self.assertEqual(EXPECTED_OVERALL_READ, data)

    def test_parse_overall_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_overall, self.tree, "domain")

    def test_parse_substance(self):
        """Asserts that a microenvironment <variable> is correctly read."""
        data = pcxml.parse_substance(
            tree=self.tree, path="microenvironment_setup", name="substrate"
        )
        self.assertEqual(EXPECTED_SUBSTANCE_READ, data)

    def test_parse_substance_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(
            ValueError, pcxml.parse_substance, self.tree, "domain", "substrate"
        )

    def test_parse_substance_wrong_substance(self):
        """Asserts that an Exception is raised when the substance name is not valid."""
        self.assertRaises(
            ValueError,
            pcxml.parse_substance,
            self.tree,
            "microenvironment_setup",
            "oxygen",
        )

    def test_parse_me(self):
        """Asserts that the <microenvironment_setup> data is correctly read."""
        data = pcxml.parse_microenvironment(
            tree=self.tree, path="microenvironment_setup"
        )
        self.assertEqual([EXPECTED_SUBSTANCE_READ], data)

    def test_parse_me_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_microenvironment, self.tree, "domain")

    def test_parse_cycle_durations(self):
        """Asserts that the <cycle> data is correctly read when durations are used."""
        data = pcxml.parse_cycle(
            tree=self.tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_DURATIONS_READ, data)

    def test_parse_cycle_rates(self):
        """Asserts that the <cycle> data is correctly read when rates are used."""
        data = pcxml.parse_cycle(
            tree=self.tree,
            path="cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_RATES_READ, data)

    def test_parse_cycle_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_cycle, self.tree, "domain")

    def test_parse_death_model(self):
        """Asserts that the data for a <death> model is correctly read."""
        data = pcxml.parse_death_model(
            tree=self.tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis",
        )
        self.assertEqual(EXPECTED_DEATH_APOPTOSIS_READ, data)

    def test_parse_death_model_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(
            ValueError, pcxml.parse_death_model, self.tree, "domain", name="apoptosis"
        )

    def test_parse_death_model_wrong_name(self):
        """Asserts that an Exception is raised when the model name is not valid."""
        self.assertRaises(
            ValueError,
            pcxml.parse_death_model,
            self.tree,
            "cell_definitions/cell_definition[@name='default']/phenotype/death",
            "pyroptosis",
        )

    def test_parse_death(self):
        """Asserts that the <death> data is correctly read."""
        expected_data = [EXPECTED_DEATH_APOPTOSIS_READ, EXPECTED_DEATH_NECROSIS_READ]
        data = pcxml.parse_death(
            tree=self.tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/death",
        )
        self.assertEqual(expected_data, data)

    def test_parse_death_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_death, self.tree, "domain")

    def test_parse_volume(self):
        """Asserts that the <volume> data is correctly read."""
        data = pcxml.parse_volume(
            tree=self.tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.assertEqual(EXPECTED_VOLUME_READ, data)

    def test_parse_volume_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_volume, self.tree, "domain")

    def test_parse_mechanics(self):
        """Asserts that the <mechanics> data is correctly read."""
        data = pcxml.parse_mechanics(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.assertEqual(EXPECTED_MECHANICS_READ, data)

    def test_parse_mechanics_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_mechanics, self.tree, "domain")

    def test_parse_motility(self):
        """Asserts that the <motility> data is correctly read."""
        data = pcxml.parse_motility(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.assertEqual(EXPECTED_MOTILITY_READ, data)

    def test_parse_motility_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(ValueError, pcxml.parse_motility, self.tree, "domain")

    def test_parse_secretion_substance(self):
        """Asserts that the <substrate> data is correctly read."""
        data = pcxml.parse_secretion_substance(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/secretion",
            name="substrate"
        )
        self.assertEqual(EXPECTED_SECRETION_READ_SUBSTRATE, data)

    def test_parse_secretion_substance_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(
            ValueError, pcxml.parse_secretion_substance, self.tree, "domain", name="substrate"
        )

    def test_parse_secretion_substance_wrong_name(self):
        """Asserts that an Exception is raised when the model name is not valid."""
        self.assertRaises(
            ValueError,
            pcxml.parse_secretion_substance,
            self.tree,
            "cell_definitions/cell_definition[@name='default']/phenotype/secretion",
            "glucose",
        )

    def test_parse_secretion(self):
        """Asserts that the <secretion> data is correctly read."""
        expected_data = [EXPECTED_SECRETION_READ_SUBSTRATE, EXPECTED_SECRETION_READ_OXYGEN]
        data = pcxml.parse_secretion(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/secretion",
        )
        self.assertEqual(expected_data, data)

    def test_parse_secretion_wrong_path(self):
        """Asserts that an Exception is raised when the wrong path is passed."""
        self.assertRaises(
            ValueError, pcxml.parse_secretion, self.tree, "domain"
        )

    def test_parse_custom(self):
        """Asserts that the custom data is correctly read."""
        data = pcxml.parse_custom(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/custom_data",
        )
        self.assertEqual(EXPECTED_CUSTOM_READ, data)


class WriteDataTest(unittest.TestCase):
    def setUp(self) -> None:
        copyfile(CONFIG_PATH, WRITE_PATH)
        self.tree = ElementTree.parse(WRITE_PATH)

    def test_write_domain(self):
        pcxml.write_domain(
            new_values=EXPECTED_DOMAIN_WRITE,
            tree=self.tree,
            path="domain",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        domain_data = pcxml.parse_domain(
            tree=new_tree,
            path="domain",
        )
        self.assertEqual(EXPECTED_DOMAIN_WRITE, domain_data)

    def test_write_overall(self):
        pcxml.write_overall(
            new_values=EXPECTED_OVERALL_WRITE,
            tree=self.tree,
            path="overall",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        overall_data = pcxml.parse_overall(
            tree=new_tree,
            path="overall",
        )
        self.assertEqual(EXPECTED_OVERALL_WRITE, overall_data)

    def test_write_substance(self):
        pcxml.write_substance(
            new_values=EXPECTED_SUBSTANCE_WRITE,
            tree=self.tree,
            path="microenvironment_setup",
            name="substrate",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        substance_data = pcxml.parse_substance(
            tree=new_tree, path="microenvironment_setup", name="substrate"
        )
        self.assertEqual(EXPECTED_SUBSTANCE_WRITE, substance_data)

    def test_write_cycle_durations(self):
        pcxml.write_cycle(
            new_values=EXPECTED_CYCLE_DURATIONS_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = pcxml.parse_cycle(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_DURATIONS_WRITE, cycle_data)

    def test_write_cycle_rates(self):
        pcxml.write_cycle(
            new_values=EXPECTED_CYCLE_RATES_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = pcxml.parse_cycle(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_RATES_WRITE, cycle_data)

    def test_write_death_model_durations(self):
        pcxml.write_death_model(
            new_values=EXPECTED_DEATH_APOPTOSIS_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        death_data = pcxml.parse_death_model(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis",
        )
        self.assertEqual(EXPECTED_DEATH_APOPTOSIS_WRITE, death_data)

    def test_write_volume(self):
        pcxml.write_volume(
            new_values=EXPECTED_VOLUME_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        volume_data = pcxml.parse_volume(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.assertEqual(EXPECTED_VOLUME_WRITE, volume_data)

    def test_write_mechanics(self):
        pcxml.write_mechanics(
            new_values=EXPECTED_MECHANICS_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        mechanics_data = pcxml.parse_mechanics(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.assertEqual(EXPECTED_MECHANICS_WRITE, mechanics_data)

    def test_write_motility(self):
        pcxml.write_motility(
            new_values=EXPECTED_MOTILITY_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        motility_data = pcxml.parse_motility(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.assertEqual(EXPECTED_MOTILITY_WRITE, motility_data)

    def test_write_custom_cell(self):
        pcxml.write_custom_data(
            new_values=EXPECTED_CUSTOM_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/custom_data",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = pcxml.parse_custom(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/custom_data",
        )
        self.assertEqual(EXPECTED_CUSTOM_WRITE, custom_data)

    def test_write_custom_user(self):
        pcxml.write_custom_data(
            new_values=EXPECTED_USER_PARAMETERS_WRITE,
            tree=self.tree,
            path="user_parameters",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = pcxml.parse_custom(
            tree=new_tree,
            path=f"user_parameters",
        )
        self.assertEqual(EXPECTED_USER_PARAMETERS_WRITE, custom_data)

    def tearDown(self) -> None:
        Path(WRITE_PATH).unlink()


if __name__ == "__main__":
    unittest.main()
