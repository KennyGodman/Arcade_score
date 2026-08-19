import { createClient, createAccount } from "genlayer-js";
import * as fs from "fs";
import * as path from "path";

/**
 * Deployment script for ArcadeScoreOracle Intelligent Contract
 */
async function deployArcadeScoreOracle() {
  console.log("Deploying ArcadeScoreOracle to GenLayer Simulator...");

  // Initialize GenLayer client
  const client = createClient({
    endpoint: process.env.GENLAYER_RPC_URL || "http://localhost:4000",
  });

  const account = createAccount(process.env.PRIVATE_KEY || "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef");

  // Read Python contract source code
  const contractPath = path.join(__dirname, "../contracts/arcade_score_oracle.py");
  const contractCode = fs.readFileSync(contractPath, "utf-8");

  // Deploy contract with constructor arguments
  const deployTx = await client.deployContract({
    account,
    code: contractCode,
    args: [account.address],
  });

  console.log(`ArcadeScoreOracle deployed successfully at address: ${deployTx.contractAddress}`);
  return deployTx.contractAddress;
}

if (require.main === module) {
  deployArcadeScoreOracle().catch((err) => {
    console.error("Deployment failed:", err);
    process.exit(1);
  });
}

export { deployArcadeScoreOracle };
