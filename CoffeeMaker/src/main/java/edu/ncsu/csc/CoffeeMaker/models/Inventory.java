package edu.ncsu.csc.CoffeeMaker.models;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.function.Function;
import java.util.stream.Collectors;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.OneToMany;

import com.fasterxml.jackson.annotation.JsonManagedReference;

@Entity
public class Inventory extends DomainObject {

    @Id
    @GeneratedValue
    private Long id;

    @OneToMany(mappedBy = "inventory", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonManagedReference("inventory-ingredient")
    private List<Ingredient> ingredients = new ArrayList<>();

    public Inventory() {
        this.ingredients = new ArrayList<>();
    }

    public Inventory(final List<Ingredient> ingredients) {
        this.ingredients = new ArrayList<>();
        for (final Ingredient igt : ingredients) {
            igt.setInventory(this);
            this.ingredients.add(igt);
        }
    }

    @Override
    public Long getId() {
        return id;
    }

    public void setId(final Long id) {
        this.id = id;
    }

    public List<Ingredient> getIngredientList() {
        return ingredients;
    }

    public boolean enoughIngredients(final Recipe r) {
        final TreeMap<String, Integer> idxMap = new TreeMap<>();
        for (int i = 0; i < ingredients.size(); i++) {
            idxMap.put(ingredients.get(i).getName(), i);
        }

        for (final Ingredient recipeIgt : r.getIngredients()) {
            final Integer idx = idxMap.get(recipeIgt.getName());
            if (idx == null || ingredients.get(idx).getUnits() < recipeIgt.getUnits()) {
                return false;
            }
        }
        return true;
    }

    public boolean useIngredients(final Recipe r) {
        if (!enoughIngredients(r)) {
            return false;
        }

        final Map<String, Ingredient> inventoryMap = ingredients.stream()
                .filter(ing -> ing.getName() != null)
                .collect(Collectors.toMap(Ingredient::getName, Function.identity(), (a, b) -> a));

        System.out.println("Recipe ingredients:");
        for (final Ingredient i : r.getIngredients()) {
            System.out.println("- " + i.getName() + ": " + i.getUnits());
        }
        for (final Ingredient recipeIng : r.getIngredients()) {
            final Ingredient invIng = inventoryMap.get(recipeIng.getName());
            if (invIng != null) {
                System.out.println("Using ingredient: " + recipeIng.getName() + " x " + recipeIng.getUnits());
                System.out.println("Before: " + invIng.getName() + " = " + invIng.getUnits());

                invIng.setUnits(invIng.getUnits() - recipeIng.getUnits());

                System.out.println("After: " + invIng.getName() + " = " + invIng.getUnits());
            } else {
                System.out.println("❌ Ingredient " + recipeIng.getName() + " not found in inventory!");
                return false;
            }
        }

        return true;
    }

    public boolean addIngredient(final String name, final Integer units) {
        if (units < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        if (ingredients.stream().anyMatch((igt) -> name.equals(igt.getName()))) {
            return false;
        }

        Ingredient newIngredient = new Ingredient(name, units);
        newIngredient.setInventory(this);
        ingredients.add(newIngredient);

        return true;
    }

    public boolean stockIngredient(final String name, final Integer units) {
        if (units < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }

        for (final Ingredient igt : ingredients) {
            if (igt.getName().equals(name)) {
                igt.setUnits(igt.getUnits() + units);
                return true;
            }
        }
        return false;
    }

    public int ingredientAmount(final String name) {
        for (final Ingredient ing : ingredients) {
            if (ing.getName().equals(name)) {
                return ing.getUnits();
            }
        }
        return -1;
    }

    @Override
    public String toString() {
        final StringBuffer buf = new StringBuffer();
        for (final Ingredient i : ingredients) {
            buf.append(i.getName());
            buf.append(": ");
            buf.append(i.getUnits());
            buf.append('\n');
        }
        return buf.toString();
    }
}
