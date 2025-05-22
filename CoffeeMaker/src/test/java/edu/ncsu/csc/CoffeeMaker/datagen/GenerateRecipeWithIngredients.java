
package edu.ncsu.csc.CoffeeMaker.datagen;

import javax.transaction.Transactional;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import edu.ncsu.csc.CoffeeMaker.TestConfig;
import edu.ncsu.csc.CoffeeMaker.models.DomainObject;
import edu.ncsu.csc.CoffeeMaker.models.Ingredient;
import edu.ncsu.csc.CoffeeMaker.models.Recipe;
import edu.ncsu.csc.CoffeeMaker.services.IngredientService;
import edu.ncsu.csc.CoffeeMaker.services.OrderService;
import edu.ncsu.csc.CoffeeMaker.services.RecipeService;

@RunWith ( SpringRunner.class )
@EnableAutoConfiguration
@SpringBootTest ( classes = TestConfig.class )
public class GenerateRecipeWithIngredients {

    @Autowired
    private RecipeService recipeService;

    @Before
    @Transactional
    public void setup () {
        recipeService.deleteAll();
    }

    @Test
    @Transactional
    public void createRecipe () {
        final Recipe r1 = new Recipe();
        r1.setName("Delicious Coffee");
        r1.setPrice(50.0);

        r1.addIngredient(new Ingredient("Coffee", 10));
        r1.addIngredient(new Ingredient("Pumpkin Spice", 3));
        r1.addIngredient(new Ingredient("Milk", 2));

        System.out.println("Ingredients before save:");
        for (Ingredient i : r1.getIngredients()) {
            System.out.println(i);
        }

        recipeService.save(r1); 

        for (final DomainObject r : recipeService.findAll()) {
            System.out.println(r);
        }
    }


}
