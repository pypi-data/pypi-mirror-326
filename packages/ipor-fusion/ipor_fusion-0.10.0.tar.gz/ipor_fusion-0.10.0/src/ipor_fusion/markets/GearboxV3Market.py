from typing import List

from web3 import Web3

from ipor_fusion.AssetMapper import AssetMapper
from ipor_fusion.ERC20 import ERC20
from ipor_fusion.MarketId import MarketId
from ipor_fusion.TransactionExecutor import TransactionExecutor
from ipor_fusion.error.UnsupportedFuseError import UnsupportedFuseError
from ipor_fusion.fuse.FuseAction import FuseAction
from ipor_fusion.fuse.GearboxSupplyFuse import GearboxSupplyFuse
from ipor_fusion.FuseMapper import FuseMapper


class GearboxV3Market:

    def __init__(
        self,
        chain_id: int,
        transaction_executor: TransactionExecutor,
        fuses: List[str],
    ):
        self._chain_id = chain_id
        self._transaction_executor = transaction_executor

        self._any_fuse_supported = False
        for fuse in fuses:
            checksum_fuse = Web3.to_checksum_address(fuse)
            if checksum_fuse in FuseMapper.map(chain_id, "GearboxV3FarmSupplyFuse"):
                self._gearbox_supply_fuse = GearboxSupplyFuse(
                    AssetMapper.map(chain_id, "dUSDCV3"),
                    FuseMapper.map(chain_id, "Erc4626SupplyFuseMarketId3")[1],
                    AssetMapper.map(chain_id, "farmdUSDCV3"),
                    FuseMapper.map(chain_id, "GearboxV3FarmSupplyFuse")[1],
                )
                self._any_fuse_supported = True

        if self._any_fuse_supported:
            self._pool = ERC20(
                transaction_executor, AssetMapper.map(chain_id, "dUSDCV3")
            )
            self._farm_pool = ERC20(
                transaction_executor, AssetMapper.map(chain_id, "farmdUSDCV3")
            )

    def is_market_supported(self) -> bool:
        return self._any_fuse_supported

    def pool(self) -> ERC20:
        return self._pool

    def farm_pool(self) -> ERC20:
        return self._farm_pool

    def supply_and_stake(self, amount: int) -> List[FuseAction]:
        if not hasattr(self, "_gearbox_supply_fuse"):
            raise UnsupportedFuseError(
                "GearboxSupplyFuse is not supported by PlasmaVault"
            )

        market_id = MarketId(GearboxSupplyFuse.PROTOCOL_ID, self._pool.address())
        return self._gearbox_supply_fuse.supply_and_stake(market_id, amount)

    def unstake_and_withdraw(self, amount: int) -> List[FuseAction]:
        if not hasattr(self, "_gearbox_supply_fuse"):
            raise UnsupportedFuseError(
                "GearboxSupplyFuse is not supported by PlasmaVault"
            )

        market_id = MarketId(GearboxSupplyFuse.PROTOCOL_ID, self._pool.address())
        return self._gearbox_supply_fuse.unstake_and_withdraw(market_id, amount)
