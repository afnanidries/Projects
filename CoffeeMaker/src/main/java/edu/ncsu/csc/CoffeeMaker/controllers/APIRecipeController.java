package edu.ncsu.csc.CoffeeMaker.controllers;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import edu.ncsu.csc.CoffeeMaker.models.Recipe;
import edu.ncsu.csc.CoffeeMaker.models.User;
import edu.ncsu.csc.CoffeeMaker.models.Ingredient;
import edu.ncsu.csc.CoffeeMaker.services.IngredientService;
import edu.ncsu.csc.CoffeeMaker.services.RecipeService;

@SuppressWarnings ( { "unchecked", "rawtypes" } )
@RestController
public class APIRecipeController extends APIController {

    @Autowired
    private RecipeService service;

    @Autowired
    private IngredientService ingredientService;

    @GetMapping ( BASE_PATH + "/recipes" )
    public List<Recipe> getRecipes () {
    	System.out.println("test hit get recipes list");
        return service.findAll();
    }

    @GetMapping ( BASE_PATH + "/recipes/{name}" )
    public ResponseEntity getRecipe ( @PathVariable ( "name" ) final String name ) {
    	System.out.println("test hit get recipes response");
        final Recipe recipe = service.findByName( name );
        return null == recipe
                ? new ResponseEntity( errorResponse( "No recipe found with name " + name ), HttpStatus.NOT_FOUND )
                : new ResponseEntity( recipe, HttpStatus.OK );
    }

    @PostMapping ( BASE_PATH + "/recipes" )
    public ResponseEntity createRecipe ( @RequestBody final Recipe recipe ) {
        System.out.println("📥 Controller hit with recipe: " + recipe);
        final Authentication a = SecurityContextHolder.getContext().getAuthentication();
        if ( !isAuthorized( a, User.STAFF ) ) {
            return new ResponseEntity( HttpStatus.FORBIDDEN );
        }

        if ( recipe.getIngredients() == null || recipe.getIngredients().size() == 0 ) {
            return new ResponseEntity( errorResponse( "Cannot add a Recipe with no Ingredients" ),
                    HttpStatus.BAD_REQUEST );
        }

        if ( recipe.getPrice() < 0 ) {
            return new ResponseEntity( errorResponse( "Price must be greater than zero." ), HttpStatus.BAD_REQUEST );
        }

        if ( recipe.getIngredients().stream().anyMatch( ( i ) -> i.getUnits() <= 0 ) ) {
            return new ResponseEntity( errorResponse( "Ingredient Amounts must be greater than zero." ),
                    HttpStatus.BAD_REQUEST );
        }

        if ( recipe.getIngredients().stream().anyMatch( ( i ) -> i.getName() == null || i.getName().length() == 0 ) ) {
            return new ResponseEntity( errorResponse( "Ingredients must all have names" ), HttpStatus.BAD_REQUEST );
        }

        if ( null != service.findByName( recipe.getName() ) ) {
            return new ResponseEntity( errorResponse( "Recipe with the name " + recipe.getName() + " already exists" ),
                    HttpStatus.BAD_REQUEST );
        }

        if ( service.findAll().size() < 3 ) {
            List<Ingredient> ingredientsToSave = new ArrayList<>();

            for (Ingredient ingredient : recipe.getIngredients()) {
                System.out.println("🧾 Incoming: " + ingredient.getName() + " | units: " + ingredient.getUnits());

                final Ingredient existing = ingredientService.findInventoryIngredientByName(ingredient.getName());

                if (existing != null && existing.getInventory() != null) {
                    System.out.println("🔁 Reusing inventory ingredient: " + existing.getName());

                    // Create a new Ingredient that copies the name, but not the inventory
                    Ingredient detached = new Ingredient();
                    detached.setName(existing.getName());
                    detached.setUnits(ingredient.getUnits()); // amount for the recipe
                    detached.setRecipe(recipe);
                    detached.setInventory(null); // avoid linking back to inventory

                    ingredientsToSave.add(detached);
                } else {
                    System.out.println("🆕 Using new ingredient: " + ingredient.getName());

                    ingredient.setRecipe(recipe);
                    ingredient.setInventory(null);
                    ingredientsToSave.add(ingredient);
                }
            }
            System.out.println("📦 Ingredients to save:");
            for (Ingredient i : ingredientsToSave) {
                System.out.println("- " + i.getName() + " | units: " + i.getUnits());
            }

            recipe.getIngredients().clear(); 
            for (Ingredient i : ingredientsToSave) {
                recipe.addIngredient(i);
            }
            System.out.println("🔍 Final ingredients in recipe before save:");
            for (Ingredient i : recipe.getIngredients()) {
                System.out.println("- " + i.getName() + " | units: " + i.getUnits() + " | recipe_id: " + i.getRecipe().getId());
            }
            service.save( recipe );
            return new ResponseEntity( successResponse( recipe.getName() + " successfully created" ), HttpStatus.OK );
        }
        else {
            return new ResponseEntity(
                    errorResponse( "Insufficient space in recipe book for recipe " + recipe.getName() ),
                    HttpStatus.INSUFFICIENT_STORAGE );
        }
    }

    @PutMapping ( BASE_PATH + "/recipes" )
    public ResponseEntity editRecipe ( @RequestBody final Recipe recipe ) {
        final Authentication a = SecurityContextHolder.getContext().getAuthentication();
        if ( isAuthorized( a, User.STAFF ) ) {
            return new ResponseEntity( HttpStatus.FORBIDDEN );
        }

        final String name = recipe.getName();
        final Recipe r = service.findByName( name );
        if ( r == null ) {
            return new ResponseEntity( errorResponse( "Recipe with the name " + name + " not found" ),
                    HttpStatus.NOT_FOUND );
        }

        try {
            r.update(recipe);

            for (Ingredient i : r.getIngredients()) {
                i.setRecipe(r);
            }

        } catch (final IllegalArgumentException e) {
            return new ResponseEntity(errorResponse(e.getMessage()), HttpStatus.BAD_REQUEST);
        }

        service.save( r );
        return new ResponseEntity( successResponse( name + " successfully updated" ), HttpStatus.OK );
    }

    @DeleteMapping ( BASE_PATH + "/recipes/{name}" )
    public ResponseEntity deleteRecipe ( @PathVariable final String name ) {
        final Authentication a = SecurityContextHolder.getContext().getAuthentication();
        if ( isAuthorized( a, User.STAFF ) ) {
            return new ResponseEntity( HttpStatus.FORBIDDEN );
        }

        final Recipe recipe = service.findByName( name );
        if ( null == recipe ) {
            return new ResponseEntity( errorResponse( "No recipe found for name " + name ), HttpStatus.NOT_FOUND );
        }
        service.delete( recipe );

        return new ResponseEntity( successResponse( name + " was deleted successfully" ), HttpStatus.OK );
    }
}