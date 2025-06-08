class RotatorCli < Formula
  include Language::Python::Virtualenv

  desc "CLI tool for automatically detecting and fixing image orientation using ML"
  homepage "https://github.com/mergd/rotator-cli"
  url "https://github.com/mergd/rotator-cli/archive/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"
  license "MIT"

  depends_on "python@3.11"
  depends_on "rust" => :build  # For some Python dependencies

  resource "check_orientation" do
    url "https://files.pythonhosted.org/packages/source/c/check_orientation/check_orientation-0.0.3.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "Pillow" do
    url "https://files.pythonhosted.org/packages/source/P/Pillow/Pillow-10.1.0.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "click" do
    url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.7.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "tqdm" do
    url "https://files.pythonhosted.org/packages/source/t/tqdm/tqdm-4.66.1.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "torch" do
    url "https://files.pythonhosted.org/packages/source/t/torch/torch-2.1.0.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "torchvision" do
    url "https://files.pythonhosted.org/packages/source/t/torchvision/torchvision-0.16.0.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/rotator", "--help"
  end
end