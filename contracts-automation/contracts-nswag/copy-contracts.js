import { existsSync, mkdirSync, copyFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Ensure output directory exists
const outputDir = join(__dirname, 'output');
if (!existsSync(outputDir)) {
  console.error('Output directory does not exist. Run "npm run generate" first.');
  process.exit(1);
}

// Copy C# client to API project
const csharpSource = join(__dirname, 'output', 'ApiClient.cs');
const csharpDestDir = join(__dirname, '..', 'api-server', 'Contracts');
const csharpDest = join(csharpDestDir, 'ApiClient.cs');

// Copy TypeScript client to React project
const tsSource = join(__dirname, 'output', 'api-client.ts');
const tsDestDir = join(__dirname, '..', 'web-client', 'src', 'contracts');
const tsDest = join(tsDestDir, 'api-client.ts');

// Ensure destination directories exist
mkdirSync(csharpDestDir, { recursive: true });
mkdirSync(tsDestDir, { recursive: true });

// Copy files
try {
  copyFileSync(csharpSource, csharpDest);
  copyFileSync(tsSource, tsDest);
  console.log('✅ Generated files copied successfully!');
  console.log(`   C# client: ${csharpDest}`);
  console.log(`   TypeScript client: ${tsDest}`);
} catch (error) {
  console.error('❌ Error copying files:', error.message);
  process.exit(1);
}
