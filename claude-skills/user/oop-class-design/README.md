# OOP Class Design (DRY + SOLID)

A Claude Code skill for designing object-oriented classes. It does not
mechanically generate classes on request — it first decides whether a class
is even the right tool, then applies SOLID and DRY when it is.

## When it triggers

Not automatically. The skill sets `disable-model-invocation: true`, which
means Claude will not decide on its own to invoke it just because a request
looks like class design. It only runs when explicitly invoked (e.g. `/oop-class-design`
or another explicit skill call) — the `description` field still documents
the intended use case (creating OOP classes, designing class hierarchies,
modeling a domain with OOP) but is not used for automatic matching while
this flag is set.

## What it does

1. **Pushes back before designing.** Checks whether the request actually
   needs state + behavior together, multiple varying instances, real
   polymorphism, and a domain noun rather than an action. If a function,
   dataclass, dict, or module would do, it says so and proposes the simpler
   alternative instead of writing the class.
2. **Applies SOLID** once a class is warranted — single responsibility,
   open/closed, Liskov substitution, interface segregation, dependency
   inversion.
3. **Applies DRY carefully** — favors composition over inheritance, only
   extracts shared base classes for genuine semantic duplication, and avoids
   premature abstraction for hypothetical future subclasses.
4. **Writes a design checklist** before coding: class list with
   responsibilities, relationships (inheritance vs. composition), public API,
   state, and an explicit note on what was deliberately _not_ made a class.
5. **Follows implementation rules**: dependencies injected via constructor,
   no wrapper getters/setters, short methods, no `Manager`/`Helper`/`Util`
   naming, and no silent no-op overrides.

## Anti-patterns it refuses

- A class with one method and no state (should be a function).
- A class with only static methods (should be a module).
- Inheritance chains deeper than two levels without clear justification.
- Subclasses that override methods to do nothing or raise
  `NotImplementedError`.
- Classes that exist only to namespace functions together.

## Output format

1. Pushback / sanity check (skipped if classes are clearly justified)
2. Design sketch (class list, relationships, public API)
3. Implementation (only after the design is agreed)

## Example usage

Invoke the skill explicitly, then describe what you want modeled:

```bash
/oop-class-design I need a ConfigLoader class that reads a YAML file and returns a dict.
```

Because the request has no state and a single method, the skill pushes back
before writing any code:

> "You asked for a `ConfigLoader` class, but it has no state and one method.
> A `load_config(path)` function would be simpler — want me to go that
> route instead?"

For a request that does need classes:

```
/oop-class-design Model a parking garage with regular, compact, and handicap spots that can be occupied or freed.
```

Here the skill proceeds to Step 2 onward, producing a design sketch (e.g. a
`ParkingSpot` base class or a composed `SpotType`, a `Garage` that owns
spots, public methods like `occupy()`/`free()`) before writing any
implementation, and confirms the design with you if it's non-trivial.
