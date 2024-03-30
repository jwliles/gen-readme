import unittest


class MyTestCase(unittest.TestCase):
  def test_get_categories(self):
    # Assuming '/home/jwl/projects/journal/til/' has specific test directories
    expected_categories = ['ack', 'amplify', 'ansible', 'bash', 'brew', 'browsers', 'chrome', 'clojure', 'css', 'deno',
                           'devops', 'docker', 'elixir', 'ember', 'gatsby', 'general', 'git', 'github',
                           'github-actions', 'go', 'groq', 'haskell', 'heroku', 'homebrew', 'html', 'http', 'inngest',
                           'internet', 'java', 'javascript', 'jq', 'kitty', 'less', 'life', 'linux', 'mac', 'mobile',
                           'mongodb', 'mysql', 'neovim', 'netlify', 'next-auth', 'nextjs', 'phoenix', 'planetscale',
                           'pnpm', 'postgres', 'powershell', 'prisma', 'python', 'rails', 'react', 'react_native',
                           'react-testing-library', 'reason', 'remix', 'ripgrep', 'rspec', 'ruby', 'security', 'sed',
                           'shell', 'sql', 'sqlite', 'streaming', 'svg', 'tailwind', 'terminal', 'testing', 'tmux',
                           'typescript', 'unix', 'urls', 'vercel', 'vim', 'vscode', 'webpack', 'workflow', 'xstate',
                           'yaml', 'zod',
                           ]  # Expected test categories
    result_categories = get_categories('/home/jwl/projects/journal/til/')
    self.assertEqual(sorted(result_categories), sorted(expected_categories))


if __name__ == '__main__':
  unittest.main()