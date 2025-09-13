"""
GreenPath CO₂ Emission Calculator
Calculates CO₂ emissions for different transport modes using IPCC emission factors
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class TransportMode(Enum):
    """Transport mode enumeration"""
    ROAD_TRUCK = "road_truck"
    ROAD_VAN = "road_van"
    RAIL = "rail"
    AIR_CARGO = "air_cargo"
    SHIP_CONTAINER = "ship_container"
    SHIP_BULK = "ship_bulk"


@dataclass
class EmissionFactor:
    """Emission factor data structure"""
    mode: TransportMode
    factor_kg_co2_per_tonne_km: float
    description: str
    source: str


class EmissionCalculator:
    """
    CO₂ emission calculator for shipments
    Formula: CO₂ = Distance × Weight × EmissionFactor
    """

    def __init__(self):
        """Initialize with IPCC and government emission factors"""
        self.emission_factors = self._load_emission_factors()
        # Debug: Print loaded factors
        print(f"Loaded emission factors: {list(self.emission_factors.keys())}")

    def _load_emission_factors(self) -> Dict[TransportMode, EmissionFactor]:
        """Load emission factors based on IPCC guidelines and government data"""
        factors = {
            TransportMode.ROAD_TRUCK: EmissionFactor(
                mode=TransportMode.ROAD_TRUCK,
                factor_kg_co2_per_tonne_km=0.062,  # kg CO₂ per tonne-km
                description="Heavy duty truck (>32 tonnes)",
                source="IPCC 2019 Guidelines"
            ),
            TransportMode.ROAD_VAN: EmissionFactor(
                mode=TransportMode.ROAD_VAN,
                factor_kg_co2_per_tonne_km=0.158,  # Higher per tonne due to smaller capacity
                description="Light commercial vehicle (<3.5 tonnes)",
                source="IPCC 2019 Guidelines"
            ),
            TransportMode.RAIL: EmissionFactor(
                mode=TransportMode.RAIL,
                factor_kg_co2_per_tonne_km=0.022,  # Very efficient
                description="Electric/diesel freight train",
                source="IPCC 2019 Guidelines"
            ),
            TransportMode.AIR_CARGO: EmissionFactor(
                mode=TransportMode.AIR_CARGO,
                factor_kg_co2_per_tonne_km=0.602,  # Highest emissions
                description="Air cargo freight",
                source="IPCC 2019 Guidelines"
            ),
            TransportMode.SHIP_CONTAINER: EmissionFactor(
                mode=TransportMode.SHIP_CONTAINER,
                factor_kg_co2_per_tonne_km=0.011,  # Most efficient
                description="Container ship",
                source="IMO Fourth GHG Study 2020"
            ),
            TransportMode.SHIP_BULK: EmissionFactor(
                mode=TransportMode.SHIP_BULK,
                factor_kg_co2_per_tonne_km=0.008,  # Very efficient for bulk
                description="Bulk carrier ship",
                source="IMO Fourth GHG Study 2020"
            )
        }
        return factors

    def calculate_emissions(
            self,
            distance_km: float,
            weight_tonnes: float,
            transport_mode: TransportMode
    ) -> Dict[str, float]:
        """
        Calculate CO₂ emissions for a shipment

        Args:
            distance_km: Distance in kilometers
            weight_tonnes: Weight in tonnes
            transport_mode: Mode of transport

        Returns:
            Dictionary with emission calculations
        """
        if transport_mode not in self.emission_factors:
            # Debug: print available keys and the requested mode
            available_modes = list(self.emission_factors.keys())
            print(f"Available modes: {available_modes}")
            print(f"Requested mode: {transport_mode} (type: {type(transport_mode)})")
            raise ValueError(
                f"Unsupported transport mode: {transport_mode}. Available: {[m.value for m in available_modes]}")

        factor = self.emission_factors[transport_mode]

        # Core calculation: CO₂ = Distance × Weight × EmissionFactor
        co2_kg = distance_km * weight_tonnes * factor.factor_kg_co2_per_tonne_km
        co2_tonnes = co2_kg / 1000

        return {
            'co2_emissions_kg': round(co2_kg, 3),
            'co2_emissions_tonnes': round(co2_tonnes, 6),
            'distance_km': distance_km,
            'weight_tonnes': weight_tonnes,
            'transport_mode': transport_mode.value,
            'emission_factor': factor.factor_kg_co2_per_tonne_km,
            'emission_factor_source': factor.source
        }

    def compare_transport_modes(
            self,
            distance_km: float,
            weight_tonnes: float,
            modes: Optional[List[TransportMode]] = None
    ) -> pd.DataFrame:
        """
        Compare CO₂ emissions across different transport modes

        Args:
            distance_km: Distance in kilometers
            weight_tonnes: Weight in tonnes
            modes: List of transport modes to compare (default: all)

        Returns:
            DataFrame with comparison results
        """
        if modes is None:
            modes = list(TransportMode)

        results = []
        for mode in modes:
            try:
                emissions = self.calculate_emissions(distance_km, weight_tonnes, mode)
                results.append({
                    'transport_mode': mode.value,
                    'co2_emissions_kg': emissions['co2_emissions_kg'],
                    'emission_factor': emissions['emission_factor'],
                    'description': self.emission_factors[mode].description
                })
            except ValueError:
                continue

        df = pd.DataFrame(results)
        if not df.empty:
            df = df.sort_values('co2_emissions_kg')
            df['emission_rank'] = range(1, len(df) + 1)
            df['emission_difference_vs_best'] = df['co2_emissions_kg'] - df['co2_emissions_kg'].min()
            df['emission_percentage_vs_best'] = (
                    (df['co2_emissions_kg'] / df['co2_emissions_kg'].min() - 1) * 100
            ).round(1)

        return df

    def calculate_carbon_tax_cost(
            self,
            co2_emissions_kg: float,
            carbon_tax_rate_per_tonne: float = 50.0
    ) -> Dict[str, float]:
        """
        Calculate carbon tax cost based on emissions

        Args:
            co2_emissions_kg: CO₂ emissions in kg
            carbon_tax_rate_per_tonne: Carbon tax rate per tonne CO₂ (default: $50)

        Returns:
            Dictionary with cost calculations
        """
        co2_tonnes = co2_emissions_kg / 1000
        carbon_tax_cost = co2_tonnes * carbon_tax_rate_per_tonne

        return {
            'co2_emissions_kg': co2_emissions_kg,
            'co2_emissions_tonnes': round(co2_tonnes, 6),
            'carbon_tax_rate_per_tonne': carbon_tax_rate_per_tonne,
            'carbon_tax_cost_usd': round(carbon_tax_cost, 2)
        }

    def get_emission_factors_table(self) -> pd.DataFrame:
        """Get emission factors as a DataFrame for display"""
        data = []
        for mode, factor in self.emission_factors.items():
            data.append({
                'transport_mode': mode.value,
                'emission_factor_kg_co2_per_tonne_km': factor.factor_kg_co2_per_tonne_km,
                'description': factor.description,
                'source': factor.source
            })

        return pd.DataFrame(data).sort_values('emission_factor_kg_co2_per_tonne_km')


class EmissionOptimizer:
    """Optimize transport mode selection for minimum emissions"""

    def __init__(self):
        self.calculator = EmissionCalculator()

    def find_greenest_option(
            self,
            distance_km: float,
            weight_tonnes: float,
            available_modes: List[TransportMode],
            max_time_penalty_percent: float = 10.0
    ) -> Dict:
        """
        Find the transport mode with lowest emissions within time constraints

        Args:
            distance_km: Distance in kilometers
            weight_tonnes: Weight in tonnes
            available_modes: Available transport modes
            max_time_penalty_percent: Maximum acceptable time penalty for green option

        Returns:
            Dictionary with recommendation
        """
        # Typical speeds for different modes (km/h)
        mode_speeds = {
            TransportMode.ROAD_TRUCK: 80,
            TransportMode.ROAD_VAN: 70,
            TransportMode.RAIL: 50,
            TransportMode.AIR_CARGO: 800,
            TransportMode.SHIP_CONTAINER: 25,
            TransportMode.SHIP_BULK: 20
        }

        options = []
        for mode in available_modes:
            emissions = self.calculator.calculate_emissions(distance_km, weight_tonnes, mode)
            speed = mode_speeds.get(mode, 50)
            travel_time_hours = distance_km / speed

            options.append({
                'mode': mode,
                'co2_emissions_kg': emissions['co2_emissions_kg'],
                'travel_time_hours': travel_time_hours,
                'emission_factor': emissions['emission_factor']
            })

        # Sort by emissions (lowest first)
        options.sort(key=lambda x: x['co2_emissions_kg'])

        if not options:
            return {'error': 'No available transport modes'}

        greenest = options[0]
        fastest = min(options, key=lambda x: x['travel_time_hours'])

        # Check if greenest option meets time constraint
        time_penalty = (greenest['travel_time_hours'] - fastest['travel_time_hours']) / fastest[
            'travel_time_hours'] * 100

        recommendation = {
            'recommended_mode': greenest['mode'].value,
            'co2_emissions_kg': greenest['co2_emissions_kg'],
            'travel_time_hours': greenest['travel_time_hours'],
            'is_within_time_constraint': time_penalty <= max_time_penalty_percent,
            'time_penalty_percent': round(time_penalty, 1),
            'emission_savings_vs_fastest': round(
                fastest['co2_emissions_kg'] - greenest['co2_emissions_kg'], 2
            ),
            'emission_reduction_percent': round(
                (1 - greenest['co2_emissions_kg'] / fastest['co2_emissions_kg']) * 100, 1
            ) if fastest['co2_emissions_kg'] > 0 else 0,
            'all_options': [
                {
                    'mode': opt['mode'].value,
                    'co2_emissions_kg': opt['co2_emissions_kg'],
                    'travel_time_hours': round(opt['travel_time_hours'], 1)
                } for opt in options
            ]
        }

        return recommendation
