import React from 'react';

export function Pokemon({ pokemon }) {
  return (
    <div classname="pokemon">
      <div classname="pokemon_name">
        <p>{pokemon.name}</p>
      </div>
      <div classname="pokemon_meta">
        <span>{pokemon.maxHP}</span>
        <span>{pokemon.maxCP}</span>
      </div>
      <div classname="pokemon_image">
        <img src={pokemon.image} alt={pokemon.name} />
      </div>
      {pokemon?.attacks?.special}
      <div classname="pokemon_attacks">
        {pokemon &&
        pokemon.attacks &&
        pokemon.attacks.special
        .slice(0, 3)
        .map(attack => (
          <span key={`${attack.name}-${attack.damage}`}>
            {attack.name}
          </span>
        ))}
      </div>
    </div>
  )
}
