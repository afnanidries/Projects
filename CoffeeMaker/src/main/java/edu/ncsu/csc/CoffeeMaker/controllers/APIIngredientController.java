package edu.ncsu.csc.CoffeeMaker.controllers;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import edu.ncsu.csc.CoffeeMaker.models.Ingredient;
import edu.ncsu.csc.CoffeeMaker.models.Inventory;
import edu.ncsu.csc.CoffeeMaker.services.IngredientService;
import edu.ncsu.csc.CoffeeMaker.services.InventoryService;

@RestController
public class APIIngredientController extends APIController {

    /**
     * RecipeService object, to be autowired in by Spring to allow for
     * manipulating the Recipe model
     */
    @Autowired
    private IngredientService ingredientService;
    
    @Autowired
    private InventoryService inventoryService;

    @SuppressWarnings({ "rawtypes", "unchecked" })
    @GetMapping ( BASE_PATH + "ingredients/{name}" )
    public ResponseEntity getIngredient ( @PathVariable final String name ) {

        final Ingredient ingr = ingredientService.findByName( name );

        if ( null == ingr ) {
            return new ResponseEntity( HttpStatus.NOT_FOUND );
        }

        return new ResponseEntity( ingr, HttpStatus.OK );
    }
    
    
    @PostMapping(BASE_PATH + "/ingredient")
    public ResponseEntity<?> createIngredient(@RequestBody final Ingredient ingredient) {
        // Check if an ingredient with the same name already exists in the global ingredient table
        if (ingredientService.findByName(ingredient.getName()) != null) {
            return new ResponseEntity<>(
                "Ingredient with the name " + ingredient.getName() + " already exists",
                HttpStatus.CONFLICT
            );
        }

        // Get current inventory
        Inventory inv = inventoryService.getInventory();

        // Check for duplicate ingredient in the inventory's ingredient list
        for (Ingredient existing : inv.getIngredientList()) {
            if (existing.getName().equalsIgnoreCase(ingredient.getName())) {
                return new ResponseEntity<>(
                    "Ingredient with the name " + ingredient.getName() + " already exists in inventory",
                    HttpStatus.CONFLICT
                );
            }
        }

        // Set inventory reference and add to the list
        Ingredient newIngredient = new Ingredient(ingredient.getName(), ingredient.getUnits());
        newIngredient.setInventory(inv);
        inv.getIngredientList().add(newIngredient);

        // Save inventory (which cascades to save the ingredient)
        inventoryService.save(inv);

        // Optional: print for debugging
        System.out.println("Current Inventory Contents:");
        for (Ingredient i : inventoryService.getInventory().getIngredientList()) {
            System.out.println(i);
        }

        return new ResponseEntity<>(newIngredient, HttpStatus.CREATED);
    }

    
    /**
     * REST API method to allow deleting a Recipe from the CoffeeMaker's
     * Inventory, by making a DELETE request to the API endpoint and indicating
     * the recipe to delete (as a path variable)
     *
     * @param name
     *            The name of the Recipe to delete
     * @return Success if the recipe could be deleted; an error if the recipe
     *         does not exist
     */
    @SuppressWarnings({ "unchecked", "rawtypes" })
	@DeleteMapping ( BASE_PATH + "/ingredients/{name}" )
    public ResponseEntity deleteIngredient ( @PathVariable final String name ) {
        final Ingredient ingr = ingredientService.findByName( name );
        if ( null == ingr ) {
            return new ResponseEntity( errorResponse( "No recipe found for name " + name ), HttpStatus.NOT_FOUND );
        }
        ingredientService.delete( ingr );

        return new ResponseEntity( successResponse( name + " was deleted successfully" ), HttpStatus.OK );
    }
    
   
}
